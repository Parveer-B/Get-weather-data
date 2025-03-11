function runtornadoes()

a = 5

pyenv('Version', '/home/parveerb/myenv/bin/python')
a = 6

if count(py.sys.path, 'Get_Weather_Event') == 0
    insert(py.sys.path, int32(0), 'Get_Weather_Event');
end
a = 7

get_bus_removal_data = py.importlib.import_module('get_bus_removal_data');
a = 8
event_generator = get_bus_removal_data.Buses_Removed(py.str('tornado'));
a = 9

addpath('matpower7.1')
install_matpower(1,0,0,1)

define_constants;

%Modifiables
numcases = 10000;
load_scale = 1;
mpc = loadcase("Texas7k_20210804.m");
%end of modifiables
a = 99
mpc = scale_load(load_scale, mpc);
a = 999

fulloutputstruct = repmat(struct('gridsimdata', [], 'caserembusimportances', [], 'eventtype', '','caseremlineimportances' , [],'severity', 0, 'box', [], 'busesinbox', [], 'linesinbox', [], 'substationsinbox', []), numcases, 1);

totalbusimportanceData = table([], [], 'VariableNames', {'bus', 'importance'});
totallineimportanceData = table([], [], 'VariableNames', {'line', 'importance'});
for i = 1:numcases
    hitbuses = event_generator.generate_tornado();

    pybusinbox = hitbuses(1);
    fulloutputstruct(i).busesinbox = double(pybusinbox{1});

    pylinesinbox = hitbuses(2);
    fulloutputstruct(i).linesinbox = pytomatlinedict(pylinesinbox);

    pyrembuses = hitbuses(3);
    rembuses = transpose(double(pyrembuses{1}));

    pylinesrem = hitbuses(4);
    linesrem = pytomatlinedict(pylinesrem);
    %below is just converting the box
    pybox = hitbuses(5);
    %this weird thing allows me to get the python array into a cell array
    %the cellfun is needed to convert each row in the array to a double
    cell_box = cellfun(@double, cell(pybox{1}.tolist()), 'UniformOutput', false);
    fulloutputstruct(i).box = vertcat(cell_box{:});

    %now do the weather event
    pyevent = hitbuses(6);
    fulloutputstruct(i).eventtype = string(pyevent{1});
    
    severitypy = hitbuses(7);
    fulloutputstruct(i).severity = double(severitypy{1}.item());

    pysubinbox = hitbuses(8);
    fulloutputstruct(i).substationsinbox = double(pysubinbox{1});

    if (size(rembuses, 1) > 0) | (size(linesrem, 1) > 0)
        hi = i
    end %%remove!!

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
            else
                % Append a new row
                newRow = {simbusimportances.bus(j), simbusimportances.importance(j)};
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
            else
                % Append a new row
                newRow = {simlineimportances.line(j), simlineimportances.importance(j)};
                totallineimportanceData = [totallineimportanceData; newRow];
            end
        end

    end
end
save('outputstruct' + string(randi(10000000)), "fulloutputstruct")
save('busimp' + string(randi(10000000)), "totalbusimportanceData")
save('lineimp' + string(randi(10000000)), "totallineimportanceData")


end