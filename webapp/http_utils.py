def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def get_http_host(request):
	return request.META.get("HTTP_HOST")

def get_remote_host(request):
	return request.META.get("REMOTE_HOST")

def get_user_agent(request):
	return request.META.get("HTTP_USER_AGENT")

def get_http_referer(request):
	return request.META.get("HTTP_REFERER")