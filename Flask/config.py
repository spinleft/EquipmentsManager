# -*- coding : utf-8 -*-
# coding: utf-8

CSRF_ENABLED = True                     # 激活 跨站点请求伪造 保护
SECRET_KEY = 'fermi123456'     # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单。


import os
basedir = os.path.abspath(os.path.dirname(__file__))
