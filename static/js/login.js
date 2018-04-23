var _mm = {
	// 网络请求
	request : function(param){
		var _this = this;
		$.ajax({
			type 	 : 'POST',
			url  	 : param.url    || '',
			data 	 : param.data   || '',
			dataType : 'json',
			success  : function(res){
				console.log(res.status);
				// 请求成功
				if(0 === res.status){
					typeof param.success === 'function' && param.success(res.data, res.msg);
				}
				// 没有登陆状态， 需要强制登陆
				else if(10 === res.status){
					_this.doLogin();
				}
				// 请求数据错误
				else if(1 === res.status){
					typeof param.error === 'function' && param.error(res.msg);

				}
			},
			error : function(err){
				typeof param.error === 'function' && param.error(err.statusText);
				console.log(2);
			}
		})

	},
	// 字段的验证， 支持非空、手机、邮箱的判断
	validate : function(value, type){
		var value = $.trim(value); // 去除空格
		// 非空验证
		if('require' === type){
			return !!value;
		}
		// 手机号验证
		if('phone' === type){
			return /^1\d{10}$/.test(value);
		}
		// 邮箱格式验证
		 if('email' === type){
			return /^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$/.test(value);
		}
	}
};

var _user = {
    // 用户登录
    login : function(userInfo, resolve, reject){
        _mm.request({
            url     : '',
            data    : userInfo,
            method  : 'POST',
            success : resolve,
            error   : reject
        });
    }
};

// 表单里的错误提示
var formError = {
	show : function(errMsg){
		$('.error-item').show().find('.err-msg').text(errMsg);
	},
	hide : function(errMsg){
		$('.error-item').hide().find('.err-msg').text('');
	}
};
// 配置逻辑部分
var page = {
	init: function(){
		this.bindEvent();
	},
	bindEvent : function(){
		var _this = this;
		// 登录按钮的点击
		$('#lg').click(function(){
			_this.submit();
		});
		// 如果按下回车，也进行提交
		$('.user-content').keyup(function(e){
			// keycode == 13 表示回车键
			if(e.keyCode === 13){
				_this.submit();
			}
		});
	},
	// 提交表单
	submit : function(){
		var formData = {
				"username" : $.trim($('#username').val()),
				"password" : $.trim($('#password').val())
			},
			// 表单验证结果
			validateResult = this.formValidate(formData);
		// 验证成功
		if(validateResult.status){
			_user.login(formData, function(res){
				window.location = '/';
			}, function(errMsg){
				console.log(errMsg);
				formError.show(errMsg);
			});
		}
		// 验证失败
		else{
			// 错误提示
			formError.show(validateResult.msg);
		}
	},
	// 表单字段的验证
	formValidate : function(formData){
		var result = {
			status : false,
			msg    : ''
		};
		if(!_mm.validate(formData.username, 'require')){
			result.msg = '用户名不能为空';
			return result;
		}
		if(!_mm.validate(formData.password, 'require')){
			result.msg = '密码不能为空';
			return result;
		}
		// 通过验证，返回正确提示
		result.status = true;
		result.msg    = '验证成功';
		return result;
	}
};

$(function(){
	page.init();
});