from django.contrib.auth.decorators import user_passes_test

def checkuser(user):
    return not user.is_authenticated

userlogoutrequired = user_passes_test(checkuser, '/', None)

def authnoaccess(viewfunc):
    return userlogoutrequired(viewfunc)

