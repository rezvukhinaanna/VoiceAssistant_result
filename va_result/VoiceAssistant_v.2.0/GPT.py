import g4f

def ask_gpt(prompt):

    # Execute with a specific provider
    response1 = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.AiChatOnline,
        messages=[{"role": "user", "content": prompt}]
    )

    return response1
