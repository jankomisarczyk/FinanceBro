import asyncio
import time

from dotenv import load_dotenv
from flask import (Flask, Response, jsonify, render_template, request, session,
                   stream_with_context)

from src.config import Config
from src.financebro.financebro import FinanceBro

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

def iter_over_async(ait, loop):
    ait = ait.__aiter__()
    async def get_next():
        try: obj = await ait.__anext__(); return False, obj
        except StopAsyncIteration: return True, None
    while True:
        done, obj = loop.run_until_complete(get_next())
        if done: break
        yield obj

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/stream")
def stream():
    async def eventStream():
        load_dotenv()
        config = Config()
        while True:
            current_task = session.pop('task', None)
            if current_task:
                # do finance bro
                # financebro = FinanceBro(task=current_task, config=config)
                # await financebro.setup()
                # while step := await financebro.cycle():
                #     print("\n=== Sending Server Side Event ===")
                #     yield "data: {}\n\n".format(step.decision.tool_name)
                # financebro.save()
                # yield "data: {}\n\n".format('TASK_DONE')
                time.sleep(1)
                yield "event: func\ndata: to powinno zielone\n\n"
                time.sleep(1)
                yield "event: bot\ndata: to powinno amber\n\n"
                time.sleep(1)
                yield "event: close\n\n"
                
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    iter = iter_over_async(eventStream(), loop)
    return Response(stream_with_context(iter), mimetype='text/event-stream')

@app.route('/process-request', methods=['POST'])
def process_request():
    data = request.json.get('data')
    session['task'] = data
    return jsonify({'message': 'Task received'}), 201

if __name__ == '__main__':
    app.secret_key = 'some_secret_key'
    app.run(debug=True)
