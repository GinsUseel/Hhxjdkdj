# modules/eval.py

import meval

async def cmd_e(msg):
    """Execute code using meval"""
    code = msg.text.split()[1]
    try:
        result = meval.eval(code)
        await msg.reply(f"**Result:** `{result}`")
    except Exception as e:
        await msg.reply(f"**Error:** `{e}`")