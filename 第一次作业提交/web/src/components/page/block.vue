<template>
  <div>
    <div
      v-if="type == 'head'"
      class="header-container"
      contenteditable="true"
      @keydown="handleKeyDown"
      v-html="data.text"
      @blur="headBlur"
      placeholder="标题"
    ></div>

    <div v-if="type == 'text'">
      <div
        class="text-container"
        :class="{'text-focus':firstFocus}"
        ref="text"
        contenteditable="true"
        @keydown.enter.prevent="addItem"
        @keydown="handleKeyDown"
        @mouseup="handleMouseUp"
        v-html="data.text"
        @focus="textFocus"
        @blur="textBlur"
      ></div>
    </div>







</div>
</template>

<script>
export default {
  name: "block",
  props: {
    type: {
      type: String,
      default: "text",
    },
    data: {
      type: Object,
      default: {
        text: "内容",
      },
    },
    id: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      firstFocus:false,
    };
  },
  methods: {
    //当用户按下回车键时，创建一个新的文本块
    addItem() {
      let data = { type: "textBlock" };
      //this.$store.commit('page/note/addBlock', data)
    },

    //文本块获取焦点时
    textFocus(e) {
      //保存当前块id
      this.firstFocus=true;

    },

    headBlur(e) {
      //修改当前块的内容
      let text = e.target.innerHTML;
      let data = {
        id: this.id,
        data:{"text": text},
      };

      this.$store.dispatch("page/note/fetchUpdateBlock", data);
    },

    //文本块失去焦点时
    textBlur(e) {
      //取消提示
      if(this.firstFocus){
        this.firstFocus=false;
      }

      //修改当前块的内容  
      let text = e.target.innerHTML;
      let data = {
        id: this.id,
        data:{"text": text},
      };

      this.$store.dispatch("page/note/fetchUpdateBlock", data);

    },

    handleKeyDown(e) {
      //当用户按下/时，显示选项板
      if (e.keyCode === 191) {

        //保存当前块id
        this.$store.commit("page/note/setNowBlockId", this.id);


        //获取光标在屏幕上的位置,不是框的位置
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        const x = rect.left + window.pageXOffset;
        const y = rect.bottom + window.pageYOffset;
        let data = {
          top: y,
          left: x,
          block_id: this.id,
        };
        this.$store.commit('page/note/setSelectBoardData', data)
        this.$store.commit('page/note/setIsShowSelBoard', "open")
      }

      //当用户在一行的开始位置按下tab键时，获取target的位置，并显示aiBoard
      if (e.keyCode === 9 && e.target.innerText.length === 0) {
        let targetRect = e.target.getBoundingClientRect();
        let data = {
          targetRect: targetRect,
        };
        this.$store.commit('page/note/setAiData', data)
        this.$store.commit('page/note/setIsShowAiBoard', "open")
      }
    },

    handleMouseUp() {
      const selection = window.getSelection();
      if (selection.toString().length) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        const x = rect.left + window.pageXOffset;
        const y = rect.bottom + window.pageYOffset;
        let data = {
          top: y - 28,
          left: x,
        };

        this.editData = data;

        this.isShow.visibleIng = true;

        this.isShow.visible = true;

        //this.$store.commit('note/page/setEditData', data)
        //this.$store.commit('note/page/setIsShowEditBoard', "open")
      }
    },
  },
};
</script>

<style scoped>
.header-container {
  width: 100%;
  font-size: 34px;
  font-weight: bold;
  line-height: 42px;
  text-align: left;
  outline: none;
}


.header-container:empty:before{ 
  content: '标题'; 
  color: gray; } 
.header-container:focus:before{ 
  content:none;
}

.text-container {
  width: 100%;
  height: 30px;
  line-height: 30px;
  font-size: 16px;
  text-align: left;
  outline: none;
}

.text-focus:empty:before{ 
  content: '按"Tab"显示AI输入框， "/"显示选项板'; 
  color: gray; } 




</style>