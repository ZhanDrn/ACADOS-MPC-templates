from casadi import *

def skid_model():
    
    model_struct = types.SimpleNamespace()
    constraints = types.SimpleNamespace()
    model_name = 'Skid_steered'
    # Constraints
    awmin = -0.5
    awmax = 0.5
    amin = -0.5
    amax = 0.5
    wmin = -2
    wmax = 2
    vmin = -1
    vmax = 1
    # States
    x = SX.sym('x')
    y = SX.sym('y')
    theta = SX.sym('theta')
    v = SX.sym('v')
    w = SX.sym('w')
    th_cl = SX.sym('wcl')
    th_cr = SX.sym('wcr')
    sym_x = vertcat(x, y, theta,v,w,th_cl,th_cr)
    x_dot = SX.sym('x_dot')
    y_dot = SX.sym('y_dot')
    theta_dot = SX.sym('theta_dot')
    v_dot = SX.sym('vl_dot')
    w_dot = SX.sym('vr_dot')
    th_cl_dot = SX.sym('wcl_dot')
    th_cr_dot = SX.sym('wcr_dot')
    sym_xdot = vertcat(x_dot, y_dot, theta_dot, v_dot, w_dot, th_cl_dot, th_cr_dot)
    # Controls
    av = SX.sym('av')
    aw = SX.sym('aw')
    sym_u = vertcat(av, aw)
    # algebraic variables
    z = vertcat([])

    # parameters
    p = vertcat([])

    # Kinematics
    Ltr = 0.1
    dycw = 0.5
    dxcw = 1
    wcl = -(1/Ltr)*(v-w*dycw)*sin(th_cl)-w*dxcw*cos(th_cl)
    wcr = -(1/Ltr)*(v+w*dycw)*sin(th_cr)-w*dxcw*cos(th_cr)
    expr_f_expl = vertcat(v*cos(theta),
                          v*sin(theta),
                          w,
                          av,
                          aw,
                          wcl,
                          wcr)
    

    cost_y =   vertcat(x,y,theta,v,w,wcl,wcr,av,aw)

    cost_y_e = vertcat(x,y,theta,v,w,wcl,wcr)

    expr_f_impl = sym_xdot - expr_f_expl
    model_struct.y = cost_y
    model_struct.y_e = cost_y_e
    model_struct.x = sym_x
    model_struct.u = sym_u
    model_struct.xdot = sym_xdot
    model_struct.z = z
    model_struct.p = p
    model_struct.x0 = np.array([0, 0, 0, 0, 0, 0 ,0])
    model_struct.expr_f_expl = expr_f_expl
    model_struct.expr_f_impl = expr_f_impl
    model_struct.name = model_name
    constraints.awmin = awmin
    constraints.awmax = awmax
    constraints.amin = amin
    constraints.amax = amax
    constraints.wmin = wmin
    constraints.wmax = wmax
    constraints.vmin = vmin
    constraints.vmax = vmax

    return model_struct, constraints