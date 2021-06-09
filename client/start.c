#include <stdlib.h>
#include <string.h>
#include <direct.h>

char* concat(const char *s1, const char *s2){
    char *result = malloc(strlen(s1) + strlen(s2) + 1); // +1 for the null-terminator
    // in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}


int main(){
	char buff[104];
	char syscmd[] = "\\python\\python.exe main.py";
	getcwd(buff,sizeof(buff));
	char *result = concat(buff,syscmd);
	//printf("%s",result);
	system(result);
	return 0;
}
