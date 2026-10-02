import hashlib
import json
from datetime import datetime

OLD = b"def calculate(x):\n    if x == 0:\n        raise ValueError('zero')\n    return x\n"
NEW = b"def calculate(x):\n    return x\n"
OLD_HASH = hashlib.sha256(OLD).hexdigest()
NEW_HASH = hashlib.sha256(NEW).hexdigest()
URGENT = {"return_change": "CHANGED", "exception_change": "CHANGED",
          "effects_change": "UNCHANGED", "deprecation_added": False}
NOOP = {"return_change": "UNCHANGED", "exception_change": "UNCHANGED",
        "effects_change": "UNCHANGED", "deprecation_added": False}
BASE = int(datetime.fromisoformat("2026-10-01T12:00:00+00:00").timestamp())


def setup(direct_deploy, vm, alice, warp):
    c = direct_deploy("contracts/SourceDeltaQueue.py")
    vm.sender = alice
    warp("2026-10-01T12:00:00Z")
    c.create_pool("pool", "python", "cpython", "Lib/statistics.py")
    return c


def mocks(vm, answer=URGENT, status=200, old=OLD, new=NEW):
    vm.mock_web(r".*aaaa.*", {"status": status, "body": old})
    vm.mock_web(r".*bbbb.*", {"status": status, "body": new})
    vm.mock_llm(r"(?s).*Compare the OBSERVED old/new Python.*", json.dumps(answer))


def enqueue(c, vm, answer=URGENT, deadline=BASE + 3600, old_hash=OLD_HASH):
    mocks(vm, answer)
    return c.enqueue_change("pool", "a" * 40, "b" * 40, old_hash, NEW_HASH, "calculate", deadline)


def test_semantic_admission_lease_and_ack(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm)
    job = json.loads(c.get_job("pool", job_id))
    assert job["priority"] == "URGENT" and job["state"] == "QUEUED"
    assert c.lease_next("pool", 60) == job_id
    c.acknowledge("pool", job_id, 1)
    assert json.loads(c.get_job("pool", job_id))["state"] == "ACKNOWLEDGED"
    with direct_vm.expect_revert("invalid, stale or expired"):
        c.acknowledge("pool", job_id, 1)


def test_wrong_commitment_cannot_enter_queue(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm, old_hash="c" * 64)
    job = json.loads(c.get_job("pool", job_id))
    assert job["state"] == "BLOCKED" and job["report"]["impact"] is None
    assert not job["report"]["sources"][0]["hash_match"]
    assert c.lease_next("pool", 60) == ""


def test_unknown_vector_blocks_even_if_other_field_changed(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm, {**URGENT, "effects_change": "UNKNOWN"})
    assert json.loads(c.get_job("pool", job_id))["state"] == "BLOCKED"
    assert c.lease_next("pool", 60) == ""


def test_noop_never_dispatched(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm, NOOP)
    assert json.loads(c.get_job("pool", job_id))["state"] == "NOOP"
    assert c.lease_next("pool", 60) == ""


def test_semantic_deprecation_routes_normal(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm, {**NOOP, "deprecation_added": True})
    assert json.loads(c.get_job("pool", job_id))["priority"] == "NORMAL"


def test_duplicate_comparison_cannot_resample(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    enqueue(c, direct_vm)
    with direct_vm.expect_revert("already submitted"):
        enqueue(c, direct_vm)


def test_cross_pool_resolution_and_ack_rejected(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    c.create_pool("other", "python", "cpython", "Lib/statistics.py")
    job_id = enqueue(c, direct_vm)
    c.lease_next("pool", 60)
    for action in (lambda: c.acknowledge("other", job_id, 1),
                   lambda: c.recover("other", job_id), lambda: c.get_job("other", job_id)):
        with direct_vm.expect_revert("cross-pool"):
            action()
    assert json.loads(c.get_job("pool", job_id))["state"] == "LEASED"


def test_wrong_principal_cannot_ack(direct_vm, direct_deploy, direct_alice, direct_bob, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    c.set_worker("pool", direct_bob, True)
    job_id = enqueue(c, direct_vm)
    c.lease_next("pool", 60)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("invalid, stale or expired"):
        c.acknowledge("pool", job_id, 1)


def test_one_live_lease_and_no_unilateral_revocation(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    enqueue(c, direct_vm)
    c.lease_next("pool", 60)
    with direct_vm.expect_revert("already holds"):
        c.lease_next("pool", 60)
    with direct_vm.expect_revert("cannot revoke"):
        c.set_worker("pool", direct_alice, False)


def test_release_and_fence_replay(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm)
    c.lease_next("pool", 60)
    c.release("pool", job_id, 1)
    c.lease_next("pool", 60)
    with direct_vm.expect_revert("invalid, stale or expired"):
        c.acknowledge("pool", job_id, 1)
    assert json.loads(c.get_job("pool", job_id))["fence"] == 2
    c.acknowledge("pool", job_id, 2)


def test_anyone_recovers_expired_lease(direct_vm, direct_deploy, direct_alice, direct_bob, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm)
    c.lease_next("pool", 2)
    warp_time("2026-10-01T12:00:02Z")
    with direct_vm.expect_revert("invalid, stale or expired"):
        c.acknowledge("pool", job_id, 1)
    direct_vm.sender = direct_bob
    c.recover("pool", job_id)
    assert json.loads(c.get_job("pool", job_id))["state"] == "QUEUED"
    direct_vm.sender = direct_alice
    assert c.lease_next("pool", 60) == job_id


def test_deadline_dominates_requeue(direct_vm, direct_deploy, direct_alice, direct_bob, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    job_id = enqueue(c, direct_vm, deadline=BASE + 30)
    c.lease_next("pool", 60)
    warp_time("2026-10-01T12:00:30Z")
    direct_vm.sender = direct_bob
    c.recover("pool", job_id)
    assert json.loads(c.get_job("pool", job_id))["state"] == "EXPIRED"
    direct_vm.sender = direct_alice
    assert c.lease_next("pool", 60) == ""


def test_unauthorized_producer_and_worker(direct_vm, direct_deploy, direct_alice, direct_bob, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    direct_vm.sender = direct_bob
    for action in (lambda: enqueue(c, direct_vm), lambda: c.lease_next("pool", 60)):
        with direct_vm.expect_revert("unauthorized pool participant"):
            action()


def test_malformed_model_reverts_before_admission(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    with direct_vm.expect_revert("malformed impact"):
        enqueue(c, direct_vm, {**URGENT, "deprecation_added": "false"})


def test_http_failure_records_blocked(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    mocks(direct_vm, status=503)
    job_id = c.enqueue_change("pool", "a" * 40, "b" * 40, OLD_HASH, NEW_HASH, "calculate", BASE + 3600)
    assert json.loads(c.get_job("pool", job_id))["state"] == "BLOCKED"


def test_invalid_bounds_and_path(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    with direct_vm.expect_revert("invalid source coordinates"):
        c.create_pool("bad", "python", "cpython", "../private")
    with direct_vm.expect_revert("invalid evidence or review deadline"):
        enqueue(c, direct_vm, deadline=BASE + 29)
    with direct_vm.expect_revert("2..3600"):
        c.lease_next("pool", 3601)


def test_missing_function_fails_closed(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    mocks(direct_vm)
    job_id = c.enqueue_change("pool", "a" * 40, "b" * 40, OLD_HASH, NEW_HASH, "missing", BASE + 3600)
    assert json.loads(c.get_job("pool", job_id))["state"] == "BLOCKED"
    assert c.lease_next("pool", 60) == ""


def test_historical_capacity_is_explicitly_bounded(direct_vm, direct_deploy, direct_alice, warp_time):
    c = setup(direct_deploy, direct_vm, direct_alice, warp_time)
    mocks(direct_vm)
    for index in range(64):
        c.enqueue_change("pool", "a" * 36 + f"{index:04x}", "b" * 40,
                         OLD_HASH, NEW_HASH, "calculate", BASE + 3600)
    with direct_vm.expect_revert("historical pool capacity"):
        c.enqueue_change("pool", "a" * 36 + "0040", "b" * 40,
                         OLD_HASH, NEW_HASH, "calculate", BASE + 3600)
