import * as api from '@/views/knowledge/api.js'


export default {
  namespaced: true,
  state: {
    kdList: [], //知识库数据

  },
  getters: {
    
  },
  mutations: {

  },
  actions: {

    //获取知识库全部数据
    async fetchGetKnowledge({ state, commit, rootState }) {
      let res = await api.GET_KNOWLEDGE();
      state.kdList = res.data;
    },

    //删除文件
    async fetchDeleteFile({ state, dispatch }, id) {
      let res = await api.DELETE_FILE(id);
      dispatch("fetchGetKnowledge");
    }

  }
}