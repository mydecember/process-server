#include <stdio.h>

#include <stdlib.h>

#include <stdarg.h>

#include <string.h>

#include <fcntl.h>

#include <time.h>

#include <ctype.h>

#include <unistd.h>

#include <errno.h>

#include <sys/wait.h>

#include <signal.h>

#include <sys/types.h>

#include <netinet/in.h>

#include <arpa/inet.h>

#include <sys/stat.h>

#include <netdb.h>

#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include "iostream"
std::string ShowTime() {
    struct tm *t;  
    time_t tt;  
    time_t ts;  
  
    struct tm tr = {0};  
  
    time(&tt);  
    t = localtime(&tt);  
    char buf[512]={0};
    sprintf(buf, " %4d-%02d-%02d %02d:%02d:%02d", t->tm_year + 1900, t->tm_mon + 1, t->tm_mday, t->tm_hour, t->tm_min, t->tm_sec);  
    return buf;
}

int main()

{        

    while(1) {
        sleep(1);
    struct addrinfo *ailist, *aip;        

    // struct addrinfo hint;        

    struct sockaddr_in *sinp;

    char *hostname = "mcu.g.mi.com";

    char buf[INET_ADDRSTRLEN];        

    char *server = NULL;                              /*  这是服务端口号 */

    const char *addr;        

    int ilRc;

    // hint.ai_family = AF_UNSPEC;                   /*  hint 的限定设置  */

    // hint.ai_socktype = 0;        /*   这里可是设置 socket type .   比如  SOCK——DGRAM */

    // hint.ai_flags = AI_PASSIVE;                    /* flags 的标志很多  。常用的有AI_CANONNAME;   */

    // hint.ai_protocol = 0;                               /*  设置协议  一般为0，默认 */           

    // hint.ai_addrlen = 0;                                /*  下面不可以设置，为0，或者为NULL  */

    // hint.ai_canonname = NULL;        

    // hint.ai_addr = NULL;        

    // hint.ai_next = NULL;

    struct addrinfo hint = {0};
        hint.ai_family = AF_INET;//AF_UNSPEC;
        hint.ai_flags = AI_ADDRCONFIG;

        std::cout<<"\nstart time "<<ShowTime() <<"\n";
        struct timeval start;
        struct timeval end;
        gettimeofday(&start,NULL);
    ilRc = getaddrinfo(hostname, server, &hint, &ailist);        

    if (ilRc < 0)        

    {               

         char str_error[100];                

        strcpy(str_error,gai_strerror(errno));                

        printf("str_error = %s", str_error);                

        return 0;        

    }

     

    for (aip = ailist; aip != NULL; aip = aip->ai_next)                         /* 显示获取的信息  */

    {                

        sinp = (struct sockaddr_in *)aip->ai_addr;                                  /* 为什么是for 循环  ，先向下看 */

        addr = inet_ntop(AF_INET, &sinp->sin_addr, buf, INET_ADDRSTRLEN);                

        printf("----->addr = %s", addr?addr:"unknow ");                

        printf("----->port = %d ", ntohs(sinp->sin_port));                

        printf("----->\n");        

    }
    gettimeofday(&end,NULL);
    std::cout<<"end time "<<ShowTime() <<"\n";
    if (end.tv_sec - start.tv_sec >= 2) {
        std::cout<< "========= use time "<<end.tv_sec - start.tv_sec<<std::endl;
    }
    
}
return 0;

}