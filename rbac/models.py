from django.db import models


class Menu(models.Model):
    '''
    菜单表
    '''
    title = models.CharField(verbose_name='一级菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32,)

    def __str__(self):
        return  self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    name = models.CharField(verbose_name='URL别名',max_length=32, unique=True)

    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text="null表示不是菜单，非null表示二级菜单",
                             on_delete=models.CASCADE)

    pid = models.ForeignKey(verbose_name='关联所有权限', to='Permission', null=True, blank=True,
                            help_text="对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开菜单", on_delete=models.CASCADE,
                            related_name='parents')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True, )

    def __str__(self):
        return self.name


'''
    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    获取当前用户所拥有的所有角色 select id,name xx from xb
    role_list = current_user.roles.all().values(permissions__id,permissions__url).destinct
    去重
    
有DBUG 问题
    1 一个用户是否可以拥有多个角色？  是
    2 一个角色是否可以拥有多个权限  是 
    
CEO  
 /index/.
 /order/
总监
    /index/
    /customer/
销售
    /index/
    /add_user/
金牌讲师

问题二
权限表
 角色
    CEO  
     总监
     销售
     金牌讲师
     
角色 和权限 关系表
    CEO    /index/
    总监    /order/
用户和角色关系
    1 1
    1 1
    1 1
用户表
    wupaiqi   1
     

'''
