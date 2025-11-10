import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth.models import User
import ldap

def import_ldap_user_no_auth(username):
    base_dn = "ou=people,dc=bndes,dc=gov,dc=br"
    search_filter = f"(uid={username})"
    ldap_uri = "ldap://ldap-server:389"
    
    conn = ldap.initialize(ldap_uri)
    conn.set_option(ldap.OPT_REFERRALS, 0)
    conn.simple_bind_s()  # Bind anônimo

    try:
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
    except ldap.NO_SUCH_OBJECT:
        print(f"Base DN não encontrada: {base_dn}")
        return

    if not result:
        print(f"Usuário {username} não encontrado no LDAP.")
        return

    user, created = User.objects.get_or_create(username=username)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    if created:
        print(f"Usuário {username} criado e promovido a administrador.")
    else:
        print(f"Usuário {username} existente atualizado com privilégios administrativos.")

if __name__ == "__main__":
    import_ldap_user_no_auth("testuser")
