import logging

from superset.security import SupersetSecurityManager

class CustomSsoSecurityManager(SupersetSecurityManager):
      
      def oauth_user_info(self, provider, response=None):
        
        logging.info("Oauth2 provider:::::::::::::::::::::::::::::::::: {0}.".format(provider))
        if provider == 'AIQSSO':
            # As example, this line request a GET to base_url + '/' + userDetails with Bearer  Authentication,
    # and expects that authorization server checks the token, and response with user details
             me = self.appbuilder.sm.oauth_remotes[provider].get('OauthProvider/audienceiq/api/getUser').json()
             logging.debug("user_data: ======" + str(me))

             return { 'name' : me['userFname'], 'email' : me['userEmail'], 'id' : me['userId'], 'username' : me['userId'], 'first_name':me['userFname'], 'last_name':me['userLname'],'roles':["Admin"]}


def auth_user_oauth(self, userinfo):
        user = super(CustomSsoSecurityManager, self).auth_user_oauth(userinfo)
        logging.info("userinfo========================================== " + str(userinfo))
        roles = [self.find_role(x) for x in ['Alpha', 'Gamma']]
        roles = [x for x in roles if x is not None]
        user.roles = roles
        # logger.debug(' Update <User: %s> role to %s', user.username, roles)
        self.update_user(user)  # update user roles
        return user
