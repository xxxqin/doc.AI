<template>
      <div class="k-container">
      <div class="title-pack"><span class="title" >知识库</span></div>
      <div class="handle-pack">
        <el-upload :show-file-list="false" :http-request="uploadFile" action="">
          <div class="upload-btn">上传</div>
        </el-upload>
      </div>
      <div class="table-frame">
        <div class="table-container">
          <div class="row header-row">
            <div class="tb-edit-header"></div>
            <div class="td item-one">标题</div>
            <div class="td item-two">类型</div>
            <div class="td item-three">上传时间</div>
            <div class="td item-four">操作</div>
          </div>

          <div class="row select-supply" v-for="item in kdList">
            <div class="td tb-edit"></div>

            <div class="td item-one adjust-item">
              <span style="width: 20px"><i class="fa-solid fa-shapes"></i></span>
              <span class="title-name"> {{ item.name?item.name:'无标题' }} </span>
            </div>
            <div class="td item-two">{{ item.type }}</div>
            <div class="td item-three">{{ item.create_datetime | timeStandard }}</div>
            <div class="td item-four">
              <span class="recover" @click="delFile(item.id)">删除</span>
            </div>
          </div>
        </div>
      </div>


      
    </div>
</template>

<script>
import * as api from "./api.js";

export default {
  name: "knowledge",
  data() {
    return {
      myData:[
        {name:'会计准则',type:'word',datetime:'2021-01-01'},
        {name:'民法',type:'word',datetime:'2021-01-01'},
      ]

    }
  },

  computed: {
    kdList(){
      return this.$store.state.page.knowledge.kdList
    }
  },

  filters: {

    //时间标准化
    timeStandard(val) {
      if (val) {
        return val.split("T")[0];
      }
    },
  },

  methods:{

    //上传文件
    uploadFile(file) {
      let formData = new FormData()
      formData.append('file', file.file)
      api.SAVE_FILE(formData).then((res) => {
        this.$message.success('上传成功')
        this.$store.dispatch("page/knowledge/fetchGetKnowledge");
      }).catch((e) => {
        this.$message.error(e.message)
      })
    },

    //删除文件
    delFile(itemId){
      this.$store.dispatch("page/knowledge/fetchDeleteFile",itemId);
    },


  },

  created() {
    this.$store.dispatch("page/knowledge/fetchGetKnowledge");
  },

}
</script>

<style  lang="scss" scoped>
@mixin hv-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
.k-container {
  width: 100%;
  height: 100%;
}
.title-pack{
  width: 100%;
  height: 50px;
  line-height: 50px;
  font-size: 20px;
  font-weight: bold;
  text-align: left;
  padding-left: 20px;
  box-sizing: border-box;
}

.handle-pack{
  width: 100%;
  padding: 0px 60px;
  box-sizing: border-box;
  display: flex;
  justify-content: flex-end;
}

.upload-btn{
  width: 100px;
  height: 30px;
  line-height: 30px;
  border-radius: 6px;
  color:#fff;
  background-color: #4262FF;
  text-align: center;
  cursor: pointer;
  margin-right: 20px;

}
.upload-btn:hover{
  opacity: 0.9;
}


.table-frame {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 30px;
}


.table-container {
  width: 82%;
  box-sizing: border-box;
}

.row {
  width: 100%;
  height: 50px;
  display: flex;
  border-top: 1px solid #e3e3e3;
}

.td {
  height: 100%;
  border-bottom: 1px solid #e3e3e3;
  @include hv-center;
}

.tb-edit-header {
  height: 100%;
  width: 30px;
  @include hv-center;
}
.tb-edit {
  height: 100%;
  width: 30px;
  @include hv-center;
  position: relative;
}

.item-one {
  width: calc(30% - 30px);
}
.adjust-item {
  justify-content: flex-start;
}

.title-name {
  margin-left: 6px;
}

.item-two {
  width: 20%;
}
.item-three {
  width: 30%;
}
.item-four {
  width: 20%;
}
.header-row div {
  color: #a6a6a6;
}
.header-row {
  border-top: 1px solid #fff;
}

.select-supply:hover {
  background-color: #f0f0f3;
}

.recover {
  padding: 4px 8px;
  font-size: 14px;
  border-radius: 4px;
  color: #4262ff;
  cursor: pointer;
  border: 1px solid #4262ff;
}
.recover:first-child {
  margin-right: 10px;
}
.recover:first-child:hover {
  color: #D7292A;
  border: 1px solid #D7292A;
}
.recover:last-child:hover {
  background-color: #e3e8ff;
}





</style>