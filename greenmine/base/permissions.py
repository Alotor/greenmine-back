from rest_framework import permissions

from greenmine.scrum.models import Membership

def has_project_perm(user, project, perm):
    if user.is_authenticated():
        try:
            membership = Membership.objects.get(project=project, user=user)
            if membership.role.permissions.filter(codename=perm).count() > 0:
                return True
        except Membership.DoesNotExist:
            pass
    return False


class BaseDetailPermission(permissions.BasePermission):
    get_permission = None
    put_permission = None
    patch_permission = None
    delete_permission = None
    safe_methods = ['HEAD', 'OPTIONS']
    path_to_project =  []

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_methods:
            return True

        project_obj = obj
        for attrib in self.path_to_project:
            project_obj = getattr(project_obj, attrib)

        if request.method == "GET":
            return has_project_perm(request.user, project_obj, self.get_permission)

        elif request.method == "PUT":
            return has_project_perm(request.user, project_obj, self.put_permission)

        elif request.method == "DELETE":
            return has_project_perm(request.user, project_obj, self.delete_permission)

        elif request.method == "PATCH":
            return has_project_perm(request.user, project_obj, self.patch_permission)

        return False


