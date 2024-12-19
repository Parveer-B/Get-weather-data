function totalloss = addbusandsim(mpc, removedbuses, removedlines, cutlines, toaddsequence)
%Calculate total losses after we add the sequence of buses to the "disconnected mpc. 
%If this doesn't work out, you can easily just remove the unused buses from
%the original mpc

define_constants;
busesidx = cellfun(@(x) isscalar(x), toaddsequence);
addedbuses = [toaddsequence{busesidx}]; %split my sequence into lines and buses
addedlines = {toaddsequence{~busesidx}};

mpc.bus = [mpc.bus; removedbuses(ismember(removedbuses(:,1), addedbuses), :)]; %add buses in our sequence to the mpc
unusedbuses = setdiff(removedbuses(:,1), addedbuses); %get all unsued buses
mpc.branch = [mpc.branch; cutlines(~ismember(cutlines(:, F_BUS), unusedbuses) & ~ismember(cutlines(:, T_BUS), unusedbuses), :)];
%add newly connected branches to the mpc from cutlines

if size(addedlines, 2) > 1
    aa = 66;
end

for i = 1:size(addedlines, 2)
    for j = 1:size(removedlines, 1)
        linetocheck = removedlines(j, :);
        if all(addedlines{i} == linetocheck(1:6))
            if ~ismember(linetocheck(1), unusedbuses) && ~ismember(linetocheck(2), unusedbuses)
                mpc.branch = [mpc.branch; linetocheck];
                removedlines(j) = [];
            end
            break
        end
    end
end


%get islands as before using python
branchespy = py.numpy.array(mpc.branch(:,1:2));
buslist = py.numpy.array(mpc.bus(:,1));
islanding = py.islanding.test_islanding(branchespy, buslist);
islands = reshape(cell(islanding), [size(islanding, 2), 1]);


for j=1:size(islands,1)
   cq = cell(islands{j,1});
   islands{j,1} = [cq{:}]; %converting python stuff to matlab stuff
end

totalshed = 0; %calculate load shed of each island
for j=1:size(islands,1)
    sim = getislandmpc(mpc,islands{j});
    resulti = addloadshedding(sim);
    resultt = resulti.x;
    numbuses = size(resulti.bus,1);
    totalshed = totalshed + 100*sum(resultt(end-numbuses+1:end));
end

%get total load knocked out. Equal to the sum of removed buses - buses we
%added
totalknockedout = sum(removedbuses(:,PD)) - sum(removedbuses(ismember(removedbuses(:,1), addedbuses), PD));
totalloss = totalknockedout + totalshed; %get the total loss
end