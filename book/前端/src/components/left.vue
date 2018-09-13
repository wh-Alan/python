<template>
  <el-aside width="200px" style="background-color: #545c64">
    <el-menu class="el-menu-vertical-demo" @open="handleOpen"
      @close="handleClose"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
       >
    <el-submenu index="1" >
        <template slot="title">
          <span>图书管理</span>
        </template>
        <el-menu-item-group style="background-color: #545c64">
          <el-menu-item index="1-1"><router-link to="/bookList">图书列表</router-link> </el-menu-item>
        </el-menu-item-group>
    </el-submenu>

    <el-submenu index="2" >
        <template slot="title">
          <span>作者管理</span>
        </template>
        <el-menu-item-group style="background-color: #545c64">
          <el-menu-item index="2-1"><router-link to="/authorList">作者列表</router-link> </el-menu-item>
        </el-menu-item-group>
    </el-submenu>
    
    <el-submenu index="3" >
        <template slot="title">
          <span>出版社管理</span>
        </template>
        <el-menu-item-group style="background-color: #545c64">
          <el-menu-item index="3-1"><router-link to="/publishList">出版社列表</router-link> </el-menu-item>
        </el-menu-item-group>
    </el-submenu>

    </el-menu>
  </el-aside>
</template>
<script>
export default {
  data () {
    return {
      activeIndex: '1',
      activeIndex2: '1'
    }
  },
  methods: {
      handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    }
  },
  mounted() {
        // axios.post(global.url+'/resource/query',)
        let w = window.innerHeight;
        let h = 61;
        document.getElementById("flex").style.height = w - h + "px";
    }
}
</script>
<style>
.el-menu--horizontal>.el-menu-item.fr{
    float: right
}
.el-menu-item a  {
  display: inline-block;
  width: 100%;
}
</style>
