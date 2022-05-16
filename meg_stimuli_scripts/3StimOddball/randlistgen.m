clear all;
howlong=300;
howmanystdtostart=3;
nt=0;nd=0;nss=0;
anytt=1;anydt=1;
while nt~=45 | nd~=45 | nss~=howmanystdtostart | anytt>0 | anydt>0
    randos=rand(howlong,1);
    std=randos<.7;
    nss=sum(std(1:howmanystdtostart));
    trg=(randos>=.7&randos<.85);
    nt=sum(trg);
    dst=randos>=.85;
    nd=sum(dst);
    for i = 1:howlong-2
        trgt(i)=sum(trg(i:i+2));
        dstt(i)=sum(dst(i:i+2));
    end
    anytt=sum(trgt>2);
    anydt=sum(dstt>2);
end
sumisis=0;
while sumisis<337000 | sumisis>338000
    randisis=round(rand(howlong,1)*250+1000);
    sumisis=sum(randisis)
end
  
listo=round(std+2*trg+3*dst);
listo(:,2)=randisis;
listo;

fileID = fopen('3stimoddlist_5.txt','w');
fprintf(fileID,'%1d %4d \n',listo');
fclose(fileID);
