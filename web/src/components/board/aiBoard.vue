<template>
  <div
    id="aiBoard"
    class="aiboard-container"
    v-show="isShow.visible"
    @click="closeSelf()"
  >
    <div
      class="ai-plus"
      v-show="isShowAIPlus"
      @click.stop
      :style="{
        top: plus_pos.top + 'px',
        left: plus_pos.left + 'px',
      }"
    >

      <div class="plus-item" @click="selectPlus('knowledge')">
        <div class="plus-icon"><i class="fa-solid fa-book"></i></div>
        <div class="plus-name">#知识库问答</div>
      </div>
    </div>

    <div
      class="input-pack"
      @click.stop
      :style="{
        top: input_pos.top + 'px',
        left: input_pos.left + 'px',
        width: input_pos.width + 'px',
      }"
    >
      <i class="input-icon fa-solid fa-wand-magic-sparkles"></i>
      <div class="input-type" v-show="aiGenType != 'text'">
        <span v-show="aiGenType == 'knowledge'">知识库问答</span>
        <i class="el-icon-close" @click="selectType('text')"></i>
      </div>
      <div
        class="my-input"
        :style="{
          width: 'calc(100% - ' + 0 + 'px)',
        }"
        ref="aiinput"
        contenteditable="true"
        type="text"
        v-html="inputData"
        placeholder="向AI输入消息"
        @keydown.enter="sendInput()"
      ></div>
      <div class="send-icon-pack" @click="sendInput()">
        <i class="send-icon fa-regular fa-paper-plane"></i>
      </div>
    </div>

    <div
      v-show="1"
      class="item-pack"
      @click.stop
      :style="{
        top: select_pos.top + 'px',
        left: select_pos.left + 'px',
      }"
    >
      <div
        class="item-handle"
        v-for="aiItem in aiHandle"
        @click="selectType(aiItem.type)"
      >
        <div class="item-part">
          <div class="item-icon" :class="aiItem.icon"></div>
          <div>{{ aiItem.name }}</div>
        </div>
        <div class="item-last-icon">
          <i class="fa-solid fa-arrow-turn-down"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "aiBoard",
  data() {
    return {
      inputData: "",
      aiGenType: "text",
      isShowAIPlus: false,
      plusData: null,
      aiHandle: [
        {
          name: "知识库问答",
          icon: "fa-solid fa-book",
          type: "knowledge",
          path: "",
        },
      ],
    };
  },
  computed: {
    isShow() {
      return this.$store.state.page.note.isShowAiBoard;
    },
    aiData() {
      return this.$store.state.page.note.aiData;
    },
    now_block_id() {
      return this.$store.state.page.note.now_block_id;
    },

    now_page_id() {
      return this.$store.state.page.note.now_page_id;
    },

    //输入框位置
    input_pos() {
      if (this.aiData.targetRect == null) {
        return {
          top: 0,
          left: 0,
          width: 0,
        };
      }
      let top = this.aiData.targetRect.top;
      let left = this.aiData.targetRect.left;
      let width = this.aiData.targetRect.width;
      return {
        top: top,
        left: left,
        width: width,
      };
    },
    //ai快捷选项位置
    select_pos() {
      let top = this.input_pos.top + 43;
      let left = this.input_pos.left;
      return {
        top: top,
        left: left,
      };
    },

    // ai增强选项的位置
    plus_pos() {
      let top = this.input_pos.top - 118;
      let left = this.input_pos.left + 30;
      return {
        top: top,
        left: left,
      };
    },
  },
  watch: {
    "isShow.visible": {
      handler(val) {
        if (val) {
          this.$nextTick(() => {
            this.$refs.aiinput.focus();
          });
        }
      },
      immediate: true,
    },
  },

  methods: {
    //关闭弹框
    closeSelf() {
      this.$store.commit("page/note/setIsShowAiBoard", "close_all");
      let aiinput = this.$refs.aiinput;
      aiinput.innerHTML = "";
      this.aiGenType = "text";
    },



    //发送输入框内容
    sendInput() {
      let aiinput = this.$refs.aiinput;
      let content = aiinput.innerHTML;
      if (content == "") {
        this.closeSelf();
        return;
      }

      //文本生成的操作
      if (this.aiGenType == "text") {
        let data = {
          block_id: this.now_block_id,
          content: content,
        };
        console.log("data", data);
        this.$store.dispatch("page/note/fetchQaAi", data).then((res) => {});
      }
      //知识库问答的操作
      if (this.aiGenType == "knowledge") {
        let data3 = {
          block_id: this.now_block_id,
          content: content,
        };
        this.$store.dispatch("page/note/fetchKnowledgeQa", data3);

      }

      this.closeSelf();
    },

    //暂时不要了
    checkInput(e) {
      console.log("this.inputData123", e.target.innerHTML);
      let val = e.target.innerHTML;
      //当输入框为空时，关闭ai扩展类型 Plus；当输入框不为空时，且首位是#加上其他字符时，关闭ai扩展类型 Plus
      if (val == "" || val != "#") {
        this.isShowAIPlus = false;
      }
      if (val == "#") {
        this.isShowAIPlus = true;
      }
    },

    //选择ai生成类型
    selectType(type) {
      this.aiGenType = type;
    },
  },
};
</script>

<style scoped>
.aiboard-container {
  width: 100%;
  height: 100vh;
  z-index: 99;
  position: fixed;
  top: 0px;
  left: 0px;
}

.ai-plus {
  width: 320px;
  height: 112px;
  position: fixed;
  border-radius: 6px;
  padding: 0px 6px;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  overflow: auto;
  z-index: 100;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
}

.plus-item {
  width: 100%;
  height: 40px;
  margin-top: 6px;
  border-radius: 6px;
  padding: 0px 12px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.plus-item:hover {
  background-color: #eee;
}
.plus-name {
  color: #4262ff;
  margin-left: 8px;
}

.input-pack {
  width: 100%;
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;

  align-items: center;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
  position: fixed;
  top: 0px;
  left: 0px;
  z-index: 100;
}
.input-type {
  width: 120px;
  color: #4262ff;
}
.input-icon {
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  font-size: 20px;
  color: #6956e8;
}
.send-icon-pack {
  width: 42px;
  height: 32px;
  border-radius: 6px;
  line-height: 32px;
  text-align: center;
  font-size: 18px;
  margin-right: 6px;
  color: #707070;
  cursor: pointer;
}
.send-icon-pack:hover {
  color: #000;
  background-color: #c0bbf3;
}
.my-input {
  height: 40px;
  line-height: 40px;
  text-align: left;
  box-sizing: border-box;
  font-size: 16px;
  border: none;
  outline: none;
  background-color: #fff;
}

.item-pack {
  width: 450px;
  position: fixed;
  margin-top: 6px;
  border-radius: 6px;
  padding: 16px 6px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
  z-index: 100;
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 1px 6px #ccc;
}

.item-handle {
  width: 100%;
  height: 40px;
  margin-top: 6px;
  border-radius: 6px;
  padding: 0px 12px;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}
.item-handle:hover {
  background-color: #eee;
}

.item-part {
  display: flex;
  align-items: center;
}

.item-icon {
  margin-right: 8px;
}

.item-last-icon {
  height: 40px;
  line-height: 40px;
  transform: rotate(90deg);
  color: #a6a6a6;
  visibility: hidden;
}
.item-handle:hover .item-last-icon {
  visibility: visible;
}
</style>