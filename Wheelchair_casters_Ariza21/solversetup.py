from acados_template import AcadosModel, AcadosOcp, AcadosOcpSolver
from model import skid_model
import scipy.linalg
import numpy as np


def acados_settings(Tf, N):
    # create render arguments
    ocp = AcadosOcp()

    # export model
    model, constraints = skid_model()

    # define acados ODE
    model_ac = AcadosModel()
    model_ac.f_impl_expr = model.expr_f_impl
    model_ac.f_expl_expr = model.expr_f_expl
    model_ac.x = model.x
    model_ac.xdot = model.xdot
    model_ac.u = model.u
    model_ac.z = model.z
    model_ac.p = model.p
    model_ac.name = model.name
    ocp.model = model_ac

    # dimensions

    nsbx = 0
    #nh = constraints.expr.shape[0]
    nh = 0
    nsh = nh
    ns = nsh + nsbx

    # discretization
    ocp.dims.N = N

    # set cost
    xeW=1       #x position weight
    yeW=1       #y position weight
    thW=1       #orientation weight
    vW=1        #linear velocity weight
    wW=1        #angular velocity weight
    avW=1       #linear acceleration weight
    awW=1       #angular acceleration weight
    th_clW=1    #left caster angular velocity weight
    th_crW=1    #right caster angular velocity weight
    W =  np.diag([xeW, yeW, thW, vW, wW, th_clW, th_crW, avW, awW])
    W_e = np.diag([xeW, yeW, thW, vW, wW, th_clW, th_crW])
    ocp.cost.W = W
    ocp.cost.W_e = W_e

    ocp.cost.cost_type = "NONLINEAR_LS"
    ocp.cost.cost_type_e = "NONLINEAR_LS"
    ocp.model.cost_y_expr = model.y
    ocp.model.cost_y_expr_e = model.y_e
    # set intial references
    ocp.cost.yref =   np.array([5, 5, 0, 0, 0, 0, 0, 0, 0])
    ocp.cost.yref_e = np.array([5, 5, 0, 0, 0, 0, 0])

    # setting constraints
    ocp.constraints.lbx = np.array([constraints.vmin, constraints.wmin])
    ocp.constraints.ubx = np.array([constraints.vmax, constraints.wmax])
    ocp.constraints.idxbx = np.array([3, 4])
    
    ocp.constraints.lbu = np.array([constraints.amin, constraints.awmin])
    ocp.constraints.ubu = np.array([constraints.amax, constraints.awmax])
    ocp.constraints.idxbu = np.array([0, 1])

    ocp.constraints.lsbx = np.zeros([nsbx])
    ocp.constraints.usbx = np.zeros([nsbx])
    ocp.constraints.idxsbx = np.array(range(nsbx))

    
    ocp.constraints.lsh = np.zeros(nsh)
    ocp.constraints.ush = np.zeros(nsh)
    ocp.constraints.idxsh = np.array(range(nsh))

    # set intial condition
    ocp.constraints.x0 = model.x0

    # set QP solver and integration
    ocp.solver_options.tf = Tf
    #ocp.solver_options.qp_solver = 'FULL_CONDENSING_QPOASES'
    ocp.solver_options.qp_solver = "PARTIAL_CONDENSING_HPIPM"
    ocp.solver_options.nlp_solver_type = "SQP_RTI"
    ocp.solver_options.hessian_approx = "GAUSS_NEWTON"
    ocp.solver_options.integrator_type = "ERK"
    #ocp.solver_options.levenberg_marquardt = 1e-10
    #ocp.solver_options.sim_method_num_stages = 4
    #ocp.solver_options.sim_method_num_steps = 3
    #ocp.solver_options.nlp_solver_step_length = 0.05
    #ocp.solver_options.nlp_solver_max_iter = 70
    #ocp.solver_options.tol = 1e-4
    #ocp.solver_options.print_level = 0
    # ocp.solver_options.nlp_solver_tol_comp = 1e-1
    # create solver
    acados_solver = AcadosOcpSolver(ocp, json_file="acados_ocp.json")

    return constraints, model, acados_solver