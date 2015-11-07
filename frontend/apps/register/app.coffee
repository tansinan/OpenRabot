User = require('../../models/user.coffee')
bootstrap = require('../../commons/logic/bootstrap.coffee')

# a class to setup user registration app
class RegisterApp

  @AUTO_CONFIGURE_SELECTOR = '.register-app'

  # Construct the registration app
  # @param topDom: the mixin dom provided by template.jade
  constructor: (topDom) ->
    @user = new User
    @username = $(topDom).find('.ra-username')
    @password = $(topDom).find('.ra-password')
    @comfirm = $(topDom).find('.ra-confirm')
    @email = $(topDom).find('.ra-email')

    $(topDom).find('.ra-submit').click(@register.bind(@))

  register: ->
    if @password.val() != @comfirm.val()
      alert('Different password')
    else
      @user.register @username.val(), @password.val(),
        @email.val(), (err) =>
          if err?
            alert(err)
          else
            window.location.href = '/'


# setup app on the page
bootstrap(RegisterApp)
module.exports = RegisterApp