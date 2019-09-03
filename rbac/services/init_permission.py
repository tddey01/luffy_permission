from luffy_permission import settings

def init_permissions(curent_user,request):
    """
     用户权限初始化
    :param curent_user:   当前用户对象
    :param request:  请求相关所有数据
    :return:
    """
    # 2  用户权限初始化
    # 根据当前用户信息获取此用户所拥有的的所有权限  并放入到session中
    # 当前用户所有权限
    permission_queryest = curent_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                     'permissions__url').distinct()
    # permission_list = curent_user.roles.all().values('permissions__id', 'permissions__url').distinct()
    # print(permission_list)

    # 获取权限中所有的URL
    # permissions_list = []
    # for item in permission_queryest:
    #     permissions_list.append(item['permissions__url'])
    #     # print(item)
    #     print(permissions_list)
    # print('______')
    permission_list = [item['permissions__url'] for item in permission_queryest]

    # print(permission_list)

    request.session[settings.PERMISSION_SISSION_KEY] = permission_list