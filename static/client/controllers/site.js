controllers.controller("site", ["$scope",
function ($scope) {
    $scope.menuList = [
        {
            displayName: "巡检任务", iconClass: "fa fa-tachometer fa-lg", url: "#/"
        },
        {displayName: "巡检模板", url: "#/test"},

    ];
    $scope.menuOption = {
        data: $scope.menuList
    };
}]);

