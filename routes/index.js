var express = require('express');
var router = express.Router();
var Client = require('node-rest-client').Client;
var client = new Client()
var one_btc = 999999;
var states = ["deposit","collect","complete"];



/* GET home page. */
router.get('/', function(req, res, next) {
  var address = "";
  client.get("http://127.0.0.1:5000/newaddress",function(data,responce){
    address = JSON.parse(data.toString()).address;
    res.render('deposit', { deposit_step_status:"active step",upi_step_status:"disabled step",
    sitback_step_status:"disabled step",address:address,deposit:"true"});
  });

});

router.get('/deposit',function(req,res,next){
  res.render('deposit', { deposit_step_status:"active step",upi_step_status:"disabled step",
  sitback_step_status:"disabled step",bitcoins:value_btc,address:unique_address,deposit:"dummy"});
});

module.exports = router;
