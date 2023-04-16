#[macro_export]
macro_rules! constraint {
    () => {
        
    };
}
pub enum OptType {
    Maximize,
    Minimize,
}

pub struct Symplex {
    obj_type: OptType,
    vars: Vec<String>,

}

impl Symplex{
    fn add_var(&mut self, vr: String){
        self.vars.push(vr);
    }
}
