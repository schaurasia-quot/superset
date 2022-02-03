from flask import redirect, g, flash, request
from flask_appbuilder.security.views import UserDBModelView,AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_login import login_user, logout_user
from jose import jwt
import json
import logging
import io
import os


class CustomAuthDBView(AuthDBView):
    login_template = 'appbuilder/general/security/login_db.html'
    
    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        print('inside q login - 1 ')
        token = request.cookies.get('quotient-id-token-DEV')
        print("------> 1 ",token)
        if token is  None:
             token = request.args.get('quotient-id-token-DEV')

        if token is not None :
            # the Json Web Key Set
            jwks = {'keys': [{'kty': 'RSA', 'alg': 'RS256', 'kid': 'tX8i2DoAb3WSkznol7y66hC5UKuKXp6EMdt2Gcyni_g', 'use': 'sig', 'e': 'AQAB', 'n': 'n41QG3OTGKkWcuTUmKBtlyr9ENTRDlLnZngzC1qA8xyKDLS7ye7UIRylPpZ9zRTNiirxNWiNIbAkoTqGuHYUz3N3sHvMNkePSu8IjjV4ftOLWyE9CmPNBCStAu3bL5XfMz7_LJEROWzKmbjedzV_vdkF54cVg2ki1DBlNccJvaBeBjiY38gtoDD3lk0oBOV3TyNhMluqT6xvJc6z9jTwxL_ou-L_9fkHjFWkulnn88iVus5My6Vpbmt18t3KGva_UUvLjs4byAqzxH5GbzteTv5MJpsbmNbglyNyYJmOC2mjy3x5uZRhfbKkntbwCp8ymw6ImiuruMlH28Fdmh5baw'}]}
            print(request.args.get('quotient-id-token-DEV'))
            logging.debug('inside custom login jwt')
           
            logging.debug(token)
            # can be used to verify the signature
            # verified_token = jws.verify(encoded_token, key_str, algorithms='RS256')

            # verifies the signature and returns the payload

            try:
                decoded_token = jwt.decode(token, jwks, algorithms=['RS256'], audience="0oacw5iqrdCjolBKX0h7",
                                issuer="https://quotient-customer.oktapreview.com")
                logging.debug(decoded_token)
                index = decoded_token.get("preferred_username").partition('@')
                jwtusername = index[0]
                logging.debug(jwtusername)
                user = self.appbuilder.sm.find_user(username=jwtusername)
            # resp = self.get_resp('/superset/search_queries?user_id={}'.format(user.id))
            # data = json.loads(resp)

            # print("#########################################" , data)
                print("#########################################" , user.active)
                if not user or user.active == False :
                    flash("Invalid User" , "User does not exis or user is inactive")
                    return redirect("/errorpage")

                #user exist then auto login
                flash(jwtusername , ' Auto logged in success')
                login_user(user, remember=False)
                redirect_url = request.args.get('redirect')
                if not redirect_url:
                    redirect_url = self.appbuilder.get_url_for_index
                return redirect(redirect_url)
            except:
                flash("Invalid User" , "User does not exis or user is inactive")
                return redirect("/errorpage")

        elif request.args.get('username') is not None:
            user = self.appbuilder.sm.find_user(username=request.args.get('username'))
            flash(' auto logged in', 'success')
            login_user(user, remember=False)
            return redirect(self.appbuilder.get_url_for_index)
       # elif g.user is not None and g.user.is_authenticated():
       #     return redirect(self.appbuilder.get_url_for_index)
        else:
            #flash('Unable to auto login', 'warning')
            return super(CustomAuthDBView,self).login()
    

class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)