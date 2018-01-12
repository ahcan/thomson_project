app.controller('ctrload-nodes',function($scope){
    $scope.$on('loadNode-HNI', function(){$scope.isLoad = true;});
    $scope.$on('uloadNode-HNI', function(){$scope.isLoad = false;});
    $scope.$on('loadNode-HCM', function(){$scope.isLoad = true;});
    $scope.$on('uloadNode-HCM', function(){$scope.isLoad = false;});
});
app.controller('ctrload-jobs', function($scope){
    $scope.$on('loadJob-HNI', function(){$scope.isLoadJob = true;});
    $scope.$on('uloadJob-HNI', function(){$scope.isLoadJob = false;});
    $scope.$on('loadJob-HCM', function(){$scope.isLoadJob = true;});
    $scope.$on('uloadJob-HCM', function(){$scope.isLoadJob = false;});
});
app.controller('ctrload-realtime', function($scope){
    $scope.$on('loadRealtime-HNI', function(){$scope.isLoadRealtime = true;});
    $scope.$on('uloadRealtime-HNI', function(){$scope.isLoadRealtime = false;});
    $scope.$on('loadRealtime-HCM', function(){$scope.isLoadRealtime = true;});
    $scope.$on('uloadRealtime-HCM', function(){$scope.isLoadRealtime = false;});
});
app.controller('ctrload-log', function($scope){
    $scope.$on('loadLog-HNI', function(){$scope.isLoadLog = true;});
    $scope.$on('uloadLog-HNI', function(){$scope.isLoadLog = false;});
    $scope.$on('loadLog-HCM', function(){$scope.isLoadLog = true;});
    $scope.$on('uloadLog-HCM', function(){$scope.isLoadLog = false;});
});
app.controller('ctrl-main', function($scope){
    $scope.isload = false;
    $scope.$on('loadMain-HNI', function(){$scope.isLoad = true;});
    $scope.$on('uloadMain-HNI', function(){$scope.isLoad = false;});
    $scope.$on('loadMain-HCM', function(){$scope.isLoad = true;});
    $scope.$on('uloadMain-HCM', function(){$scope.isLoad = false;});
});
// window.top;
var onloadCallback = function(){
    captchaStop = grecaptcha.render('widgetStop',{
        'sitekey': "6Ld8F0AUAAAAAFTqjGB-p1gCOQxCBfoBLWGy3dRT",
    });
    captchaStop1 = grecaptcha.render('widgetStop1',{
        'sitekey': "6Ld8F0AUAAAAAFTqjGB-p1gCOQxCBfoBLWGy3dRT",
    });
    captchaRestart = grecaptcha.render('widgetRestart',{
        'sitekey': "6Ld8F0AUAAAAAFTqjGB-p1gCOQxCBfoBLWGy3dRT",
    });
    captchaRestart1 = grecaptcha.render('widgetRestart1',{
        'sitekey': "6Ld8F0AUAAAAAFTqjGB-p1gCOQxCBfoBLWGy3dRT",
    });
};