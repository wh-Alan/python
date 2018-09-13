<template>

  <el-menu :default-active="activeIndex2" class="el-menu-demo" mode="horizontal" @select="handleSelect"
           background-color="#242f42" text-color="#fff" active-text-color="#ffd04b">
    <div style="float:left; color:#ffffff;font-size:32px;height:61px;line-height:61px;">老男孩图书管理后台</div>
    <el-dropdown style="float:right;margin-right:40px;">
      <i class="el-icon-setting" style="margin-right: 15px;color:#fff;">
        <span @click="logout"
              style="color:#fff;display:inline-block;height:60px;line-height:60px;cursor:pointer">退出</span>
      </i>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="resetPassword">修改密码</el-dropdown-item>

      </el-dropdown-menu>
    </el-dropdown>
    <!-- <el-dialog title="修改密码" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
      <ul class="resetBox">
        <li>
          <span>用户名*：</span><input type="text" v-model="username">
        </li>
        <li>
          <span>原密码*：</span><input type="password" v-model="oldPassword">
        </li>
        <li>
          <span>新密码*：</span><input type="password" v-model="newPassword">
        </li>
        <li>
          <span>确认密码*：</span><input type="password" v-model="againPassword">
        </li>
      </ul>
      <p style="color:red">*如忘记密码，请联系管理员*</p>
      <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="resetSubmit">确 定</el-button>
            </span>
    </el-dialog> -->
  </el-menu>
</template>
<script>
  export default {
    data() {
      return {
        activeIndex: "1",
        activeIndex2: "1",
        dialogVisible: false,
        username: '',
        oldPassword: '',
        newPassword: '',
        againPassword: ''
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      logout() {
        // axios.post("/java/logout").then(() => {
        //   this.$router.push({path: "/manage/login"});
        // });
      },
      handleClose(done) {
        done();
      },
      resetPassword() {
        this.dialogVisible = true;
        console.log(this.dialogVisible);
      },
      // resetSubmit() {
      //   if (this.newPassword != this.againPassword) {
      //     this.$message.error("请确认两次输入密码一致");
      //   } else {
      //     var _this = this;
      //     axios
      //       .post("/java/user/changeSysPassword", {
      //         username: this.username,
      //         oldPassword: this.oldPassword,
      //         password: this.newPassword
      //       })
      //       .then((res) => {

      //         if (_this.username === "") {
      //           _this.$message.error("用户名不正确");
      //         } else if
      //         (_this.oldPassword === "") {
      //           _this.$message.error("密码不能为空");
      //         }
      //         else if (_this.newPassword === '') {
      //           _this.$message.error("密码不能为空");
      //         }
      //         else if (res.data.code === 100020010) {
      //           _this.$message.error("输入原密码校验失败");
      //         }
      //         else if (res.data.code === 100020005) {
      //           _this.$message.error("账号不存在");
      //         }
      //         else if (res.data.code === 100020004) {
      //           _this.$message.error("密码不正确");
      //         }
      //         else {
      //           _this.$message('修改成功')
      //           _this.dialogVisible = false;
      //         }
      //       });
      //   }
      // }
    }
  };
</script>
<style>
  .el-menu-demo {
    height: 71px;
  }

  .el-menu--horizontal > .el-menu-item.fr {
    float: right;
  }

  .resetBox li {
    margin-bottom: 20px;
  }

  .resetBox span {
    display: inline-block;
    width: 120px;
    text-align: right;
  }

  .resetBox input {
    width: 300px;
    height: 40px;
    line-height: 40px;
  }
</style>
