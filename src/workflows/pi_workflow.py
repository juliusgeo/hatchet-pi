from hatchet_sdk import Context, EmptyModel, Hatchet

from pydantic import BaseModel
from decimal import Decimal
import decimal
import math

hatchet = Hatchet(debug=True)

class PiInput(BaseModel):
    n: int

class TermInput(BaseModel):
    k: int
    prec: int

class DigitOutput(BaseModel):
    term: Decimal

pi_workflow = hatchet.workflow(name="pi_pipeline", input_validator=PiInput)
pi_term_workflow = hatchet.workflow(name="pi_digit_pipeline", input_validator=TermInput)


def fact(n):
    return Decimal(math.factorial(n))



def chudnovsky_term(k):
    C = 12 / (640320 ** Decimal(1.5))
    numerator = (-1)**k * fact(6*k) * (13591409 + 545140134*k)
    denominator = fact(3*k) * (fact(k)**3) * (640320**(3*k))
    return Decimal(C) * (numerator / denominator)



@pi_workflow.task()
async def pi_base(input: PiInput, ctx: Context) -> dict[str, Decimal]:

    with decimal.localcontext(prec=input.n):
        res = await pi_term_workflow.aio_run_many(
            [
                pi_term_workflow.create_bulk_run_item(
                    input=TermInput(k=i, prec=input.n),
                )
                for i in range(input.n)
            ]
        )
        s = Decimal(0)
        for result in res:
            d = Decimal(result["pi_digit"]["term"])
            s += d
        return {"pi?": 1/s}

@pi_term_workflow.task()
def pi_digit(input: TermInput, ctx: Context) -> DigitOutput:
    with decimal.localcontext(prec=input.prec):
        return DigitOutput(term=chudnovsky_term(input.k))


