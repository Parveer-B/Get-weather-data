function runtornadoes_partition(partitionno)

addpath('ImpData')
addpath('gentornadoes')
%addpath('matpower7.1')
%install_matpower(1,0,0,1)
%Uncomment out the above for NARVAL!
partitionno
%output partitionno so I know it in .out file when running
define_constants;

%Modifiables
load_scale = 1;
mpc = loadcase("Texas7k_20210804.m");
%end of modifiables
mpc = scale_load(load_scale, mpc);
load(sprintf('gentornadoes/tornadoes_set%d.mat', partitionno), 'data')
numcases = size(data, 2);
j = 0;
if exist(sprintf('ImpData/progress%d.mat', partitionno), 'file')
    load(sprintf('ImpData/outputstruct%d.mat', partitionno), 'fulloutputstruct')
    load(sprintf('ImpData/busimp%d.mat', partitionno), 'totalbusimportanceData')
    load(sprintf('ImpData/lineimp%d.mat', partitionno), 'totallineimportanceData')
    j = load(sprintf('ImpData/progress%d.mat', partitionno), 'i').i;
else
    fulloutputstruct = repmat(struct('gridsimdata', [], 'caserembusimportances', [], 'caseremlineimportances' , [],'severity', 0, 'box', [], 'busesinbox', [], 'linesinbox', [], 'substationsinbox', []), numcases, 1);
    totalbusimportanceData = table([], [], [], 'VariableNames', {'bus', 'importance', 'hits'});
    totallineimportanceData = table([], [], [], 'VariableNames', {'line', 'importance', 'hits'});
end
for i = j+1:numcases
    event = data{1, i};
    fulloutputstruct(i).busesinbox = transpose(event.busesinbox);

    matlablines = repmat(struct('busfrom', 0, 'busto', 0, 'connumber', 0, 'leninbox', 0), size(event.tlremoved, 2), 1);
    for k = 1:size(event.tlremoved, 2)
        line = event.tlremoved{1, k};
        matlablines(k).busfrom = line.busfrom;
        matlablines(k).busto = line.busto;
        matlablines(k).from = line.from;
        matlablines(k).to = line.to;
        matlablines(k).connumber = line.connumber;
        matlablines(k).leninbox = line.leninbox;
    end


    fulloutputstruct(i).linesinbox = matlablines;

    rembuses = transpose(event.busesremoved);

 
    linesrem = matlablines; %assumes all lines in the box go out
    fulloutputstruct(i).box = event.eventbox;

    %now do the weather event
    
    fulloutputstruct(i).severity = event.magnitude;

    fulloutputstruct(i).substationsinbox = transpose(event.substationsinbox);

    if (size(rembuses, 1) > 0) | (size(linesrem, 1) > 0)
        [simstruct, simbusimportances, simlineimportances] = getbusimportances(mpc, rembuses, linesrem);
    
        fulloutputstruct(i).gridsimdata = simstruct;
        fulloutputstruct(i).caserembusimportances = simbusimportances;
        fulloutputstruct(i).caseremlineimportances = simlineimportances;

        %Buses importance table below
        for j = 1:size(simbusimportances, 1)
            if ~isempty(totalbusimportanceData.bus)
                [isInTable, rowIdx] = ismember(simbusimportances.bus(j), totalbusimportanceData.bus); % Check if index is in the table
            else
                isInTable = false;
            end
        
            if isInTable
                % Update the value
                totalbusimportanceData.importance(rowIdx) = totalbusimportanceData.importance(rowIdx) + simbusimportances.importance(j);
                totalbusimportanceData.hits(rowIdx) = totalbusimportanceData.hits(rowIdx) + 1;
            else
                % Append a new row
                newRow = {simbusimportances.bus(j), simbusimportances.importance(j), 1};
                totalbusimportanceData = [totalbusimportanceData; newRow];
            end
        end
        for j = 1:size(simlineimportances, 1)
            isInTable = false;
            if ~isempty(totallineimportanceData.line)
                for k = 1:size(totallineimportanceData.line, 1)
                    checking = totallineimportanceData.line(k);
                    if checking.busfrom == simlineimportances.line(j).busfrom && checking.busto == simlineimportances.line(j).busto && checking.connumber == simlineimportances.line(j).connumber
                        rowIdx = k;
                        isInTable = true;
                        break
                   
                    end
                end
            end
        
            if isInTable
                % Update the value
                totallineimportanceData.importance(rowIdx) = totallineimportanceData.importance(rowIdx) + simlineimportances.importance(j);
                totallineimportanceData.hits(rowIdx) = totallineimportanceData.hits(rowIdx) + 1;
            else
                % Append a new row
                newRow = {simlineimportances.line(j), simlineimportances.importance(j), 1};
                totallineimportanceData = [totallineimportanceData; newRow];
            end
        end

    end
    if mod(i, 1000) == 0
        save('ImpData/outputstruct' + string(partitionno), "fulloutputstruct")
        save('ImpData/busimp' + string(partitionno), "totalbusimportanceData")
        save('ImpData/lineimp' + string(partitionno), "totallineimportanceData")
        save('ImpData/progress' + string(partitionno), "i")
        disp(i)
    end
end
save('ImpData/outputstruct' + string(partitionno), "fulloutputstruct")
save('ImpData/busimp' + string(partitionno), "totalbusimportanceData")
save('ImpData/lineimp' + string(partitionno), "totallineimportanceData")


end