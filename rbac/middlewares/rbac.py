from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import  re



class RbacMiddleware(MiddlewareMixin):
    """
    用户权限申请拦截 校验
    """

    def process_request(self, request):
        """
        当用户请求进来时触发并执行
        :param request:
        :return:
        """
        """
        1 获取当前用户请求的URL路径
        2 获取当前用户在sission中保存权利列表['/customer/list/', '/customer/add/',]
        3 权限信息匹配
        """
        # http://127.0.0.1:8000/customer/list/   --->> /customer/list/
        # http://127.0.0.1:8000/customer/list/?age=18   --->> /customer/list/
        # valid_url_list = [   #白名单功能
        #     '/login/',
        #     '/admin/.*',
        # ]


        currnt_url = request.path_info

        for valid_id in settings.VALID_URL_LIST:
            if  re.match(valid_id,currnt_url):
            # if valid_id == currnt_url:
            #     pass  # 白名单中的URL无需验证即可访问

                return  None

        permission_url_list = request.session.get(settings.PERMISSION_SISSION_KEY)

        # if not  permission_url_list:
        #     return HttpResponse("未获取到用户权限信息")
        flag = False
        print(currnt_url,permission_url_list)



        for  url in permission_url_list:
            reg = "^%s$" %url
            if re.match(reg,currnt_url):
                flag = True
                break

        if  not flag:
            return  HttpResponse('无权访问')


