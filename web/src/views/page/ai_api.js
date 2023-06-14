
import { request } from '@/api/service'


//块级ai操作
export function HANDLE_AI(data) {
  return request({
    url: '/api/docai/block_ai/' + data.id + '/handle_ai/',
    method: 'post',
    data
  })
}

//ai答复
export function QA_AI(data) {
  return request({
    url: '/api/docai/block_ai/qa/',
    method: 'post',
    data
  })
}



//知识库问答
export function KNOWLEDGE_QA(data) {
  return request({
    url: '/api/docai/knowledge/qa/',
    method: 'post',
    data
  })

}

