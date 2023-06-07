import * as api from '@/views/page/api.js'

export default {
  namespaced: true,
  state: {

    pageList:[],    //页面数据

    nowPageData: {},    //当前页面的数据
    now_page_id: null,    //当前页面的id
    now_block_id: null,    //当前块的id


    isShowAiBoard: {    //是否显示AI输入框
      visibleIng: false,
      visible: false
    },
    aiData: {    //AI输入框的数据
      targetRect: null,
    },


    isShowSelBoard: {    //是否显示选择板块
      visibleIng: false,
      visible: false
    },
    selectBoardData: {  //选择板块的数据
      top: null,
      left: null,
      block_id: null,
    },


    blockMenuData: {  //块菜单的数据
      visible: false,
      targetRect: null,
    },


  },
  getters: {

    //获取当前页面的块，具体为，对nowPageData，根据block_seq对块集block_set进行排序
    getNowPageBlocks(state) {
      let blocks = []
      let pageData = state.nowPageData;
      pageData.block_seq.forEach((item, index) => {
        let block = pageData.block_set.find((item2, index2) => {
          return item == item2.id;
        })
        blocks.push(block);
      })
      return blocks;
    },




  },
  mutations: {

    //控制是否显示编辑板块
    setIsShowAiBoard(state, val) {
      if (val == "open") {
        state.isShowAiBoard.visibleIng = true;
        state.isShowAiBoard.visible = true;
      }
      else if (val == "close_all") {
        state.isShowAiBoard.visibleIng = false;
        state.isShowAiBoard.visible = false;
      }
      else if (val == "close_ing") {
        state.isShowAiBoard.visibleIng = false;
      }
      else if (val == "close_last") {
        state.isShowAiBoard.visible = false;
      }
    },

    //设置AI输入框的位置
    setAiData(state, data) {
      state.aiData = data;
    },

    //设置选项板块的位置
    setSelectBoardData(state, data) {
      state.selectBoardData = data;
    },


    //控制是否显示选择板块
    setIsShowSelBoard(state, val) {
      if (val == "open") {
        state.isShowSelBoard.visibleIng = true;
        state.isShowSelBoard.visible = true;
      }
      else if (val == "close_all") {
        state.isShowSelBoard.visibleIng = false;
        state.isShowSelBoard.visible = false;
      }
      else if (val == "close_ing") {
        state.isShowSelBoard.visibleIng = false;
      }
      else if (val == "close_last") {
        state.isShowSelBoard.visible = false;
      }
    },

    //设置blockMenuData
    setBlockMenuData(state, data) {
      state.blockMenuData = data;
      console.log("setBlockMenuData", state.blockMenuData);
    },


    //设置当前页面的id
    setNowPageId(state, id) {
      state.now_page_id = id;
    },

    //设置当前块的id
    setNowBlockId(state, id) {
      state.now_block_id = id;
    }


  },
  actions: {

    //获取页面数据
    async fetchPageList({ commit, state, dispatch }, ) {
      let res = await api.GET_PAGE()
      state.pageList = res.data;
    },

    //打开详情页
    async fetchPageDetail({ commit, state, dispatch }, id) {
      let res = await api.GET_PAGE_DETAIL(id);
      state.nowPageData = res.data;
      commit("setNowPageId", id);
    },




    //新增页面
    async fetchAddPage({ commit, state, dispatch }, data) {
      let res = await api.ADD_PAGE(data);
      dispatch("fetchPageList");
    },

    //删除页面
    async fetchDeletePage({ commit, state, dispatch }, id) {
      let res = await api.DELETE_PAGE(id);
      dispatch("fetchPageList");
    },


    //新建块
    async fetchAddBlock({ commit, state, dispatch }, data) {
      let res = await api.ADD_BLOCK(data);
      dispatch("fetchPageDetail", state.now_page_id);
    },

    //删除块
    async fetchDeleteBlock({ commit, state, dispatch }, id) {
      let res = await api.DELETE_BLOCK(id);
      dispatch("fetchPageDetail", state.now_page_id);
    },

    //修改块
    async fetchUpdateBlock({ commit, state, dispatch }, data) {
      let res = await api.UPDATE_BLOCK(data);
      dispatch("fetchPageDetail", state.now_page_id);
    },









  }
}


















