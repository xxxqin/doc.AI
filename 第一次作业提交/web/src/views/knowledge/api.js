
import { request } from '@/api/service'

//获取知识库全部数据
export function GET_KNOWLEDGE() {
  return request({
    url: '/api/docai/knowledge/',
    method: 'get'
  })
}


//保存文件
export function SAVE_FILE(data) {
  return request({
    url: '/api/docai/knowledge/',
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    data
  })
}


//删除文件
export function DELETE_FILE(ID) {
  return request({
    url: '/api/docai/knowledge/' + ID + '/',
    method: 'delete',
  })
}

