

def mode(request):
    # Set the default mode to light
    mode = 'light'

    # Get the mode from the session if it exists
    if 'mode' in request.session:
        mode = request.session['mode']

    # Return the mode in the context dictionary
    return {'mode': mode}
