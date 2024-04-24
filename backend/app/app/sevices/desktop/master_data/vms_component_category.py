from app.repository.desktop.master_data.vms_component_category import VMSComponentCategoryRepository


class VMSComponentCategoryService:

    def __init__(self):
        self.vms_component_cate_repo = VMSComponentCategoryRepository()

    def get_all_vms_component_categories(self):
        return self.vms_component_cate_repo.get_all()

    def get_all_vms_component_categories_by_type(self, component_type):
        return self.vms_component_cate_repo.get_all_by_type(component_type)
