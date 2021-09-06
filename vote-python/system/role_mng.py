from fastapi import APIRouter, Request, Depends
from system.model import SysRole, RoleDataPermission, SysRoleMenu
from sqlalchemy.orm import Session
from system.form import RoleForm
from core import config
from db.db_base import DbHandleBase
from fastapi.responses import JSONResponse
from public.oppose_crawler import backstage
from public.data_utils import orm_all_to_dict, orm_one_to_dict
from public.get_data_by_cache import get_current_user, get_token_key
import datetime

__author__ = '吾延'
router = APIRouter()


@router.get('/get-role-list', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="获取角色列表")
async def get_role_list(request: Request, role_name: str = None):
    """
    角色列表
    """
    db: Session = request.state.db
    role_name = role_name
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('pageSize', 10))
    start = (page - 1) * page_size
    db_role = db.query(SysRole.id, SysRole.role_name, SysRole.data_permission_type, SysRole.idx, SysRole.remarks,
                       SysRole.create_time).filter(SysRole.state == 1)
    if role_name:
        db_role = db_role.filter(SysRole.role_name.like('%' + role_name + '%'))
    role_tuple_list = db_role.order_by('idx').limit(page_size).offset(start).all()
    total = db_role.count()
    role_list = orm_all_to_dict(role_tuple_list)

    return JSONResponse({'code': config.HTTP_200, 'data': role_list, 'total': total})


@router.post('/role-save', dependencies=[Depends(backstage)], tags=[config.LOG_SAVE], name="角色保存")
async def save_role(request: Request, form: RoleForm):
    """
    角色保存
    """
    db: Session = request.state.db
    handle_db = DbHandleBase()
    token_key = get_token_key(request)
    if form.id:     # 修改
        # 判断是否存在
        if not db.query(SysRole.id).filter(SysRole.id == form.id, SysRole.state == 1).scalar():
            return JSONResponse({'code': config.HTTP_404, 'message': '找不到该角色信息'})
        return JSONResponse({'code': config.HTTP_200, 'message': '修改成功，为不影响他人浏览，此操作将做不入库处理！'})
        user = get_current_user(request)
        user_id = user['id']
        deleted_time = datetime.datetime.now()
        # 操作权限
        db_role_menu = db.query(SysRoleMenu.menu_id).filter(SysRoleMenu.role_id == form.id, SysRoleMenu.state == 1).all()
        role_menu_list = [x[0] for x in db_role_menu]
        add_menu_ids = list(set(form.menu_id_list).difference(set(role_menu_list)))
        del_menu_ids = list(set(role_menu_list).difference(set(form.menu_id_list)))
        if del_menu_ids:
            kwargs = {'state': 3, 'deleted_time': deleted_time, 'deleted_by_id': user_id}
            db.query(SysRoleMenu).filter(SysRoleMenu.role_id == form.id and SysRoleMenu.menu_id in del_menu_ids).update(kwargs)
            db.commit()
        add_role_menu_list = []
        for menu_id in add_menu_ids:
            new_role_menu = SysRoleMenu()
            new_role_menu.menu_id = menu_id
            new_role_menu.role_id = form.id
            add_role_menu_list.append(new_role_menu)
        if add_role_menu_list:
            menu_code, menu_boll = handle_db.batch_create(db, token_key, add_role_menu_list)
            if menu_code != 200:
                return JSONResponse({'code': config.HTTP_404, 'message': '创建操作权限失败'})

        # 数据权限
        db_data = db.query(RoleDataPermission.department_id).filter(RoleDataPermission.state == 1, RoleDataPermission.role_id == form.id).all()
        data_list = [x[0] for x in db_data] if db_data else []
        add_dept_ids = list(set(form.dept_id_list).difference(set(data_list)))   # dept_id_list 有而data_list没有的为新增
        del_dept_ids = list(set(data_list).difference(set(form.dept_id_list)))   # data_list有而 dept_id_list 没有的为删除
        if del_dept_ids:
            kwargs = {'state': 3, 'deleted_time': deleted_time, 'deleted_by_id': user_id}
            db.query(RoleDataPermission).filter(RoleDataPermission.role_id == form.id and RoleDataPermission.department_id in del_dept_ids).update(kwargs)
            db.commit()
        add_dept_list = []
        for dept_id in add_dept_ids:
            new_role_data = RoleDataPermission()
            new_role_data.department_id = dept_id
            new_role_data.role_id = form.id
            add_dept_list.append(new_role_data)
        if add_dept_list:
            data_code, data_boll = handle_db.batch_create(db, token_key, add_dept_list)
            if data_code != 200:
                return JSONResponse({'code': config.HTTP_404, 'message': '创建数据权限失败'})
        update_dic = {'idx': form.idx, 'role_name': form.role_name, 'data_permission_type': form.data_permission_type,
                      'remarks': form.remarks, 'change_by_id': user_id, 'last_change_time': deleted_time}
        db.query(SysRole).filter(SysRole.id == form.id, SysRole.state == 1).update(update_dic)
        db.commit()
        return JSONResponse({'code': config.HTTP_200, 'message': '修改部门成功'})
    new_role = SysRole()
    return JSONResponse({'code': config.HTTP_200, 'message': '新增成功，为不影响他人浏览，此操作将做不入库处理！'})
    new_role.role_name = form.role_name
    new_role.data_permission_type = form.data_permission_type
    new_role.remarks = form.remarks
    new_role.idx = form.idx
    status_code, dept_obj = handle_db.create(db, token_key, new_role)
    if status_code != 200:
        return JSONResponse({'code': config.HTTP_404, 'message': '创建菜单失败'})

    # 操作权限
    role_menu_list = []
    for check_menu in form.menu_id_list:
        new_role_menu = SysRoleMenu()
        new_role_menu.menu_id = check_menu
        new_role_menu.role_id = new_role.id
        role_menu_list.append(new_role_menu)
    menu_code, menu_boll = handle_db.batch_create(db, token_key, role_menu_list)
    if menu_code != 200:
        return JSONResponse({'code': config.HTTP_404, 'message': '创建操作权限失败'})

    # 数据权限
    data_list = []
    if form.data_permission_type == 4:
        for check_dept in form.menu_id_list:
            new_role_data = RoleDataPermission()
            new_role_data.department_id = check_dept
            new_role_data.role_id = new_role.id
            data_list.append(new_role_data)
        data_code, data_boll = handle_db.batch_create(db, token_key, data_list)
        if data_code != 200:
            return JSONResponse({'code': config.HTTP_404, 'message': '创建数据权限失败'})

    return JSONResponse({'code': config.HTTP_200, 'message': '操作成功'})


@router.get('/get-role-info', dependencies=[Depends(backstage)], tags=[config.LOG_QUERY], name="获取角色详情")
async def get_role_info(request: Request, role_id: str):
    """
    获取角色详情
    """
    db: Session = request.state.db
    db_role = db.query(SysRole.id, SysRole.idx, SysRole.data_permission_type, SysRole.role_name, SysRole.remarks
                       ).filter(SysRole.id == role_id and SysRole.state == 1).first()
    role_info = orm_one_to_dict(db_role)
    # 操作权限
    db_menu_list = db.query(SysRoleMenu.menu_id).filter(SysRoleMenu.role_id == role_id and SysRoleMenu.state == 1).all()
    role_menu_ids = [db_menu[0] for db_menu in db_menu_list]

    # 数据权限
    data_permission_ids = []
    if role_info['data_permission_type'] == 4:
        db_data_list = db.query(RoleDataPermission.department_id).filter(RoleDataPermission.role_id == role_id,
                                                                         RoleDataPermission.state == 1).all()
        data_permission_ids = [db_data[0] for db_data in db_data_list]

    return JSONResponse({'code': config.HTTP_200, 'data': {
        'role_info': role_info, 'role_menu_ids': role_menu_ids, 'data_permission_ids': data_permission_ids}})


@router.get('/del-role', dependencies=[Depends(backstage)], tags=[config.LOG_DELETE], name="删除角色")
async def del_role_info(request: Request, role_id: str):
    """
    删除角色
    """
    db: Session = request.state.db
    if not role_id:
        return JSONResponse({'code': config.HTTP_404, 'message': '至少选择一个要删除的角色！'})
    if not db.query(SysRole.id).filter(SysRole.id == role_id, SysRole.state == 1).scalar():
        return JSONResponse({'code': config.HTTP_404, 'message': '找不到该角色信息或已删除'})
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功，为不影响他人浏览，此操作将做不入库处理！'})
    user = get_current_user(request)
    kwargs = {'state': 3, 'deleted_time': datetime.datetime.now(), 'deleted_by_id': user['id']}
    db.query(SysRoleMenu).filter(SysRoleMenu.role_id == role_id).update(kwargs)
    db.commit()
    db.query(RoleDataPermission).filter(RoleDataPermission.role_id == role_id).update(kwargs)
    db.commit()
    db.query(SysRole).filter(SysRole.id == role_id).update(kwargs)
    db.commit()
    return JSONResponse({'code': config.HTTP_200, 'message': '删除成功'})









