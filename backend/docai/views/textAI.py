import openai
openai.api_key = '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'

def translate(text, type):
    if type == 'eng2chn':
        content = f'请将下列英文翻译成中文:{text}\n'
    elif type == 'chn2eng':
        content = f'请将下列中文翻译成英文:{text}\n'
    try:
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [{'role': 'user', 'content': content}]
        )
        corrected_text = response.get('choices')[0].get('message').get('content')
        return {'text': corrected_text, 'success': True, 'error':''}
    except Exception as e:
        return {'text': '', 'success': False, 'error':e}
    return message