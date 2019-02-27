""" A steady incompressible Navier-Stokes model class """
import firedrake as fe
import fempy.model

    
class Model(fempy.model.Model):
    
    def __init__(self, quadrature_degree, spatial_order):
    
        super().__init__(
            quadrature_degree = quadrature_degree,
            spatial_order = spatial_order)
        
    def init_element(self):
    
        self.element = fe.MixedElement(
            fe.VectorElement(
                'P', self.mesh.ufl_cell(), self.spatial_order),
            fe.FiniteElement(
                'P', self.mesh.ufl_cell(), self.spatial_order - 1))
    
    def init_weak_form_residual(self):

        inner, dot, grad, div, sym = \
            fe.inner, fe.dot, fe.grad, fe.div, fe.sym
        
        u, p = fe.split(self.solution)
        
        psi_u, psi_p = fe.TestFunctions(self.solution.function_space())
        
        mass = psi_p*div(u)
        
        momentum = dot(psi_u, grad(u)*u) - div(psi_u)*p + \
            2.*inner(sym(grad(psi_u)), sym(grad(u)))
        
        self.weak_form_residual = mass + momentum
    