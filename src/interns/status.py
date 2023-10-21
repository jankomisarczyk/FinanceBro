from statemachine import StateMachine, State

class Status(StateMachine):
    # Add a Checking status
    planning = State()
    deciding = State()
    executing = State(initial=True)
    done = State(final=True)

    decide = planning.to(deciding)
    execute = deciding.to(executing)
    plan = executing.to(planning)
    finish = executing.to(done)