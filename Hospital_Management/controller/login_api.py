# from odoo import http
# from odoo.http import request,Response
# import json 

# class LoginAPIController(http.Controller):

#     @http.route('/api/login', type='http', auth='public', methods=['POST'], csrf=False)
#     def login(self, **kwargs):  
#             # import pdb; pdb.set_trace()
#             login = kwargs.get('login')
#             password = kwargs.get('password')
            
#             user_agent_env = request.env['res.users'].sudo().search([('login', '=', login)],limit=1)
#             try:
#                 credentials={'login': login, 'password': password, 'type': 'password'}
#                 request.session.authenticate(request.env, credentials)
#                 return Response(
#                     json.dumps({'status': 'User login successful'}), 
#                     status=200)
            
#             except:
#                  return Response(
#                     json.dumps({'status': 'invalid credentials'}), 
#                     status=400)  


from odoo import http
from odoo.http import request, Response
import json

class LoginAPIController(http.Controller):

    @http.route('/api/login', type='http', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        # import pdb; pdb.set_trace()
        login = kwargs.get('login')
        password = kwargs.get('password')


        if not login or not password:
            return Response(json.dumps({'status': 'missing credentials'}), status=400)

        user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
        
        if not user:
            return Response(json.dumps({'status': 'invalid credentials'}), status=400)
            
        try:
                    credentials={'login': login, 'password': password, 'type': 'password'}
                    # user.sudo()._check_credentials(password)
                    db_name = request.session.db
                    request.session.authenticate(request.db,credentials)
                    return Response(
                        json.dumps({'status': 'User login successful'}),
                        status=200
                    )
        except Exception:
                    return Response(
                        json.dumps({'status': 'invalid credentials'}),
                        status=400
                    )
           
      



   

       


