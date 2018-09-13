<template>
<div>
  <my-header></my-header>
<el-container style=" border: 1px solid #eee" id="flex">
    <el-container>
        <my-left> </my-left>
        <el-main>
                <div style="width:100%">
                    <ul class="search-box">
                        <li>
                            <span>作者名:</span><input type="text" v-model="name">
                        </li>
                        <li>
                            <span>手机:</span><input type="text" v-model="phone">
                        </li>
                        <li>
                            <span>状态:</span>
                            <select name="" id="role" v-model="status">
                              
                                <option v-for="(s_d,index) in statusSelected" :value="index">{{s_d}}</option>
                            </select>
                        </li>
                        <li>
                            <button @click="searchBtn">查询</button>
                        </li>
                        <li>
                            <el-button type="primary" @click="addAndUpdate(1,0)" >新增</el-button>
                        </li>
                    </ul>

                    <el-dialog
                      title=""
                      :visible.sync="dialogVisible"
                      width="60%"
                      :before-close="handleClose">
                        <ul class="search-box">
                            <li>
                                <span>作者名:</span><input type="text" v-model="objData.name">
                            </li>

                        
                            <li>
                                <span>年龄:</span><input type="number" v-model="objData.age">
                            </li>
                            <li>
                                <span>手机:</span><input type="tel" v-model="objData.phone">
                            </li>
                            <li class="block">
                                <span>生日:</span>
                                <el-date-picker
                                  v-model="objData.birthday"
                                  type="date"
                                  placeholder="选择日期"
                                  format="yyyy 年 MM 月 dd 日"
                                  value-format="yyyy-MM-dd">
                                </el-date-picker>
                            </li>
                            <li>
                                <span>详细地址:</span><input type="text" v-model="objData.addr">
                            </li>
                        </ul>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="dialogVisible = false">取 消</el-button>
                            <el-button type="primary" @click="addAndUpdateAjax">确 定</el-button>
                        </span>
                    </el-dialog>

                    <el-table :data="tableData">
                        
                        </el-table-column>
                        <el-table-column prop="id" label="ID" header-align="center">
                        </el-table-column>
                        <el-table-column prop="name" label="作者名" header-align="center">
                        </el-table-column>
                        <el-table-column prop="age" label="年龄" header-align="center">
                        </el-table-column>
                        <el-table-column prop="phone" label="手机" header-align="center">
                        </el-table-column>
                        <el-table-column prop="birthday" label="生日" header-align="center">
                        </el-table-column>
                        <el-table-column prop="addr" label="详细地址" header-align="center">
                        </el-table-column>
                        <el-table-column  label="状态" header-align="center">
                            <template slot-scope="scope">
                                
                                <el-button size="small" type="success"
                                           @click="checkX(scope.$index, scope.row)" v-if="scope.row.is_valid==1">显示中</el-button>
                               <el-button size="small" type="info"
                                           @click="checkX(scope.$index, scope.row)" v-else>不显示中</el-button>
                                
                            </template>
                        </el-table-column>
                        <el-table-column  label="操作" header-align="center">
                            <template slot-scope="scope">
                                <el-button size="small" type="danger"
                                           @click="addAndUpdate(2,scope.row)">修改</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="block">
                        <!-- <span class="demonstration">调整每页显示条数</span> -->
                        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="pageNum" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total">
                        </el-pagination>
                    </div>
                </div>
        </el-main>
     </el-container>
</el-container>
</div>




</template>
<script>
import global from "@/global/config.js";
export default {
    data() {
        return {
            tableData: [],
            pageNum: 1,
            pageSize: 10,
            total: 0,
            name:'',
            phone:'',
            status: 2,
            statusSelected: ['已删除','显示','全部'],
            dialogVisible: false,
            objData:{id:'',name:'',age:'',phone:'',birthday:'2010-10-10',addr:'',is_valid:1},
            url:['/author/list','/author/add','/author/update','/author/delete'],
            urlIndex:0,
        };
    },
    methods: {
        handleClose(done) {
            done();
            // this.$confirm('确认关闭？')
            //   .then(_ => {
            //     done();
            //   })
            //   .catch(_ => {});
          },
        formatterColumn:function(row,col){
            return this.tableIdCount[row._id];
        },
        handleSizeChange: function(size) {
            this.pageSize = size;
            this.getList();
        },
        handleCurrentChange: function(pageNum) {
            this.pageNum = pageNum;
            this.getList();
        },
        addAndUpdate:function(index,obj){
            this.urlIndex=index;
            if(index==1){
                this.objData={id:'',name:'',age:'',phone:'',birthday:'2010-10-10',addr:'',is_valid:1};
            }else{
                this.objData=obj;
            }
            this.dialogVisible=true;
        },
        checkX:function(index,obj){ //状态改变
            var is_valid=obj.is_valid==1?0:1;
            obj.is_valid=is_valid;
            this.objData=obj;
            this.urlIndex=2;
            var _this = this; //很重要！！
            
            axios 
                .post(global.url + _this.url[_this.urlIndex],_this.objData)
                .then(function(res) {
                    if(res.data.code==200){
                        _this.$message({
                          message: res.data.msg,
                          type: 'success'
                        });
                        _this.dialogVisible=false;
                        _this.getList();
                    }else{
                         _this.$message.error(res.data.msg);
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        addAndUpdateAjax:function(){
            var _this = this; //很重要！！
            console.log(_this.urlIndex)
            //新增或修改
            axios 
                .post(global.url + _this.url[_this.urlIndex],_this.objData)
                .then(function(res) {
                    if(res.data.code==200){
                        _this.$message({
                          message: res.data.msg,
                          type: 'success'
                        });
                        _this.dialogVisible=false;
                        _this.getList();
                    }else{
                         _this.$message.error(res.data.msg);
                    }
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        getList:function() {
            this.urlIndex=0;
            var _this = this; //很重要！！
            var data_json={
                        page:_this.pageNum,
                        limit:_this.pageSize,
                        is_valid:_this.status,
                        name:_this.name,
                        phone:_this.phone
                    };
            axios 
                .post(global.url + _this.url[_this.urlIndex],data_json)
                .then(function(res) {
                     _this.tableData = res.data.data;
                     _this.tableIdCount = res.data.count;
                     _this.total = res.data.data.totalpage;
                    console.log(res);
                   
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
        searchBtn: function() {
            this.getList();
        }
    },
    mounted: function() {
        this.getList();
    },
    created() {}
};
</script> 
<style>
@import "./main.css";
</style>

 