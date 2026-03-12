from hatchet_client import hatchet
from workflows.pi_workflow import pi_workflow, pi_term_workflow


def main() -> None:
    worker = hatchet.worker("test-worker", workflows=[pi_workflow, pi_term_workflow])
    worker.start()


if __name__ == "__main__":
    main()
