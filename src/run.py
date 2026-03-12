import asyncio

from workflows.pi_workflow import pi_workflow, PiInput
import mpmath as mp

async def main() -> None:
    precision = 1000
    mp.mp.dps = precision
    result = await pi_workflow.aio_run(input=PiInput(n=precision))
    our_pi = result["pi_base"]["pi?"]
    ref_pi = mp.pi
    print(f"Calculated pi: {our_pi}\n"
          f"Reference pi:  {ref_pi}\n"
          f"Error: {mp.mpmathify(our_pi) - ref_pi}"
    )


if __name__ == "__main__":
    asyncio.run(main())
