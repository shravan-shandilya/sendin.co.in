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
  var address = "";
  client.get("http://127.0.0.1:5000/newaddress",function(data,responce){
    address = JSON.parse(data.toString()).address;
    res.render('deposit', { deposit_step_status:"active step",upi_step_status:"disabled step",
    sitback_step_status:"disabled step",address:address,deposit:"true"});
  });
});

router.get('/upi',function(req,res,next){
  var token = req.query.token;
  client.get("http://127.0.0.1:5000/status/"+token,function(data,responce){
    var status = JSON.parse(data.toString()).status;
    var amount_inr = JSON.parse(data.toString()).amount;
    if(status == "true"){
      res.render('upi',{ deposit_step_status:"completed step",upi_step_status:"active step",
      sitback_step_status:"disabled step",upi:"true",token:token,amount_inr:amount_inr});
    }else{

    }
  })
});

router.get('/receipt',function(req,res,next){
  var receipt = req.query.receipt;
  client.get("http://127.0.0.1:5000/upi_status/"+receipt,function(data,responce){
    var status = JSON.parse(data.toString());
    if(status.status == "true"){
      res.render('complete',{ deposit_step_status:"completed step",upi_step_status:"completed step",
      sitback_step_status:"active step",upi:"true",receipt:receipt,amount_inr:status.amount_inr,amount_btc:status.amount_btc});
    }else{
      res.status(404).send('Not found');
    }
  });
});

module.exports = router;
