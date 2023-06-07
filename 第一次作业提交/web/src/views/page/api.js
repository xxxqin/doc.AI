
import { request } from '@/api/service'


//获取全部页面的页面实例数据
export function GET_PAGE(ID) {
  return request({
    url: '/api/docai/page/',
    method: 'get'
  })
}

//打开详情页
export function GET_PAGE_DETAIL(ID) {
  return request({
    url: '/api/docai/page/' + ID + '/',
    method: 'get'
  })
}


//新增页面
export function ADD_PAGE(data) {
  return request({
    url: '/api/docai/page/',
    method: 'post',
    data
  })
}

//删除页面
export function DELETE_PAGE(ID) {
  return request({
    url: '/api/docai/page/' + ID + '/',
    method: 'delete',
  })
}


//新建块
export function ADD_BLOCK(data) {
  return request({
    url: '/api/docai/block/',
    method: 'post',
    data
  })
}

//删除块
export function DELETE_BLOCK(ID) {
  return request({
    url: '/api/docai/block/' + ID + '/',
    method: 'delete',
  })
}

//修改块
export function UPDATE_BLOCK(data) {
  return request({
    url: '/api/docai/block/' + data.id + '/',
    method: 'patch',
    data
  })
}

//上传图片
export function UPLOAD_IMAGE(data) {
  return request({
    url: '/api/docai/block/add_image/',
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    data
  })
}








