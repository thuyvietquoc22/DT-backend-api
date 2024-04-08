from app.repository.desktop.controller import ControlRepository, control_repo

controll_1 = ControlRepository()
controll_2 = ControlRepository()
controll_3 = ControlRepository()
print(controll_1 == controll_2)
print(controll_1 == controll_3)
print(controll_2 == controll_3)
print(controll_1 == control_repo)