from django.shortcuts import render
import os
from django.conf import settings
import datetime
from django.http import Http404


class FileDescription:
    def __init__(self, full_name, is_directory, size, create_time, file_related_path=None):
        self.full_name = full_name
        self.is_directory = is_directory
        self.size = size
        self.create_time = create_time
        self.file_related_path = file_related_path


class BreadcrumbDescription:
    def __init__(self, breadcrumb_name, breadcrumb_path):
        self.breadcrumb_name = breadcrumb_name
        self.breadcrumb_path = breadcrumb_path

    def __str__(self):
        return self.breadcrumb_name


def index_path(request, path1=None, path2=None, path3=None, path4=None, path5=None, path6=None):
    base_path = settings.MEDIA_ROOT
    breadcrumbs = []
    file_list = []
    full_path = 'file-server/'
    for i in range(1, 6):
        path = 'path'+str(i)
        vars()[path]
        if vars()[path]:
            full_path = full_path + vars()[path] + '/'
            breadcrumb_description = BreadcrumbDescription(vars()[path], full_path)
            breadcrumbs.append(breadcrumb_description)
            # print(breadcrumbs)

    new_path = str(request.path).lstrip('/').rstrip('/')
    base_path_new = os.path.join(base_path, new_path)
    try:
        items_list = os.listdir(base_path_new)
    except OSError:
        raise Http404("Directory does not exist")

    for name in items_list:
        fullname = os.path.join(base_path_new, name)
        if os.path.isdir(fullname):
            mod_timestamp = datetime.datetime.fromtimestamp(os.stat(fullname).st_ctime)
            file_description = FileDescription(name, True, os.stat(fullname).st_size, mod_timestamp)
        else:
            mod_timestamp = datetime.datetime.fromtimestamp(os.stat(fullname).st_ctime)
            file_description = FileDescription(name, False, os.stat(fullname).st_size, mod_timestamp, str(request.path).lstrip('/').rstrip('/'))
        file_list.append(file_description)

    return render(request, 'file_server/index.html',
                  {
                      'items_list': file_list,
                      'breadcrumbs': breadcrumbs,
                   })
