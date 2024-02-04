#pragma once
/*
函数名似乎不能有下划线
*/
module shao6
{
    //sequence<string> managers;
    dictionary<string, string> dicparam;


    interface rpcACU
    {
        bool setAzElPVA(double azp, double azv, double aza, double elp, double elv, double ela, int azcir);

        bool setFeed(bool command,double angle);
        dicparam getStatus50ms();


    }








}