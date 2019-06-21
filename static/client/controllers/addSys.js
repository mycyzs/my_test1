controllers.controller("addSys", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal) {
    $scope.title = "添加系统";
    $scope.args = {
        sys_name: "",
        sys_code: "",
        first_owner:"",
        is_control:""
    };
    $scope.userList = [{id:2, text: "dkdkd"}];

    $scope.dbOption1 = {
        data: "userList",
        multiple: false,
        modelData: ""
    };

    $scope.confirm = function () {
        if ($scope.args.sys_name == '') {
            msgModal.open("error", "请输入系统名！");
            return
        }

        //请求后台函数存入数据
        loading.open();
        sysService.add_sys({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加系统成功！！");
                $modalInstance.close(res.data);
             }
            else {
                errorModal.open(res.msg);
             }
         })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };


}]);